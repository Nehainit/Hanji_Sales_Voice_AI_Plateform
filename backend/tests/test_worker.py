"""The call worker, with local Redis for the queue, a fake database and a fake dialer."""
import threading
import time
from datetime import datetime

from app.scheduler.planning import plan_first_call
from app.scheduler.queue import IST
from app.scheduler.rules import CallSettings
from app.scheduler.worker import CallResult, Worker


def at(day, hour, minute=0):
    return datetime(2026, 10, day, hour, minute, tzinfo=IST)


class Clock:
    def __init__(self, t):
        self.t = t

    def __call__(self):
        return self.t


class FakeDB:
    def __init__(self, *orders):
        self.orders = {o["id"]: dict(o) for o in orders}
        self.calls = []
        self._lock = threading.Lock()

    def get_order(self, order_id):
        return dict(self.orders[order_id]) if order_id in self.orders else None

    def update_order(self, order_id, **fields):
        self.orders[order_id].update(fields)
        return self.orders[order_id]

    def save_call(self, call):
        with self._lock:
            self.calls.append(call)
        return call

    def get_call_settings(self, store_id):
        return None  # defaults: 9 AM–9 PM, 3 tries, 2 hours apart


def order(n=1, created=None, phone=None):
    return {"id": f"order-{n}", "store_id": "store-1", "status": "pending",
            "customer_phone": phone or f"98290{n:05d}", "created_at": (created or at(6, 10, 0)).isoformat()}


class Dialer:
    """Fake phone call: returns the given results in turn and counts calls."""
    def __init__(self, *results):
        self.results = list(results)
        self.calls = 0

    def __call__(self, order, attempt):
        self.calls += 1
        return self.results.pop(0) if len(self.results) > 1 else self.results[0]


NOT_ANSWERED = CallResult(status="not_answered")


# Task 4.4 / spec scheduler/call-scheduling: Unanswered calls are retried
def test_three_unanswered_calls_end_as_no_answer_with_no_fourth_call(queue):
    db, clock, dialer = FakeDB(order()), Clock(at(6, 10, 5)), Dialer(NOT_ANSWERED)
    worker = Worker(queue, dialer, db, now=clock)
    plan_first_call(queue, db.orders["order-1"], CallSettings())

    worker.run_once()
    assert queue.planned("order-1") == [(2, at(6, 12, 5))]
    clock.t = at(6, 12, 5)
    worker.run_once()
    assert queue.planned("order-1") == [(3, at(6, 14, 5))]
    clock.t = at(6, 14, 5)
    worker.run_once()

    assert dialer.calls == 3
    assert db.orders["order-1"]["status"] == "no_answer"
    assert queue.planned("order-1") == []
    clock.t = at(7, 12, 0)
    assert worker.run_once() == 0 and dialer.calls == 3


def test_retry_after_calling_hours_moves_to_next_morning(queue):
    db, clock = FakeDB(order()), Clock(at(6, 20, 0))
    queue.plan("order-1", 1, at(6, 20, 0))
    Worker(queue, Dialer(NOT_ANSWERED), db, now=clock).run_once()
    assert queue.planned("order-1") == [(2, at(7, 9, 0))]


def test_busy_and_failed_calls_are_retried_too(queue):
    db, clock = FakeDB(order()), Clock(at(6, 12, 0))
    queue.plan("order-1", 1, at(6, 12, 0))
    Worker(queue, Dialer(CallResult(status="busy")), db, now=clock).run_once()
    assert queue.planned("order-1") == [(2, at(6, 14, 0))]


def test_a_crashing_call_counts_as_failed_and_is_retried(queue):
    def broken(order, attempt):
        raise RuntimeError("network down")
    db, clock = FakeDB(order()), Clock(at(6, 12, 0))
    queue.plan("order-1", 1, at(6, 12, 0))
    Worker(queue, broken, db, now=clock).run_once()
    assert db.calls[0]["status"] == "failed" and db.calls[0]["error"] == "network down"
    assert queue.planned("order-1") == [(2, at(6, 14, 0))]


def test_unanswered_calls_are_saved_as_no_answer(queue):
    db, clock = FakeDB(order()), Clock(at(6, 12, 0))
    queue.plan("order-1", 1, at(6, 12, 0))
    Worker(queue, Dialer(NOT_ANSWERED), db, now=clock).run_once()
    assert (db.calls[0]["attempt_no"], db.calls[0]["status"], db.calls[0]["outcome"]) == (1, "not_answered", "no_answer")


# Results that settle the order
def test_confirmed_order_gets_no_more_calls(queue):
    db, clock = FakeDB(order()), Clock(at(6, 10, 5))
    queue.plan("order-1", 1, at(6, 10, 5))
    Worker(queue, Dialer(CallResult(status="answered", outcome="confirmed", duration_seconds=42)), db, now=clock).run_once()
    assert db.orders["order-1"]["status"] == "confirmed"
    assert queue.planned("order-1") == []


def test_cancelled_order_saves_reason(queue):
    db, clock = FakeDB(order()), Clock(at(6, 10, 5))
    queue.plan("order-1", 1, at(6, 10, 5))
    result = CallResult(status="answered", outcome="cancelled", cancel_reason="Ordered by mistake")
    Worker(queue, Dialer(result), db, now=clock).run_once()
    assert db.orders["order-1"]["status"] == "cancelled"
    assert db.calls[0]["cancel_reason"] == "Ordered by mistake"


def test_order_closed_before_its_call_is_not_dialled(queue):
    db, clock, dialer = FakeDB(order()), Clock(at(6, 10, 5)), Dialer(NOT_ANSWERED)
    queue.plan("order-1", 1, at(6, 10, 5))
    db.orders["order-1"]["status"] = "cancelled"
    Worker(queue, dialer, db, now=clock).run_once()
    assert dialer.calls == 0


# Callbacks (task 4.5 is verified later with a real test call)
def test_callback_at_7pm_is_planned_for_7pm(queue):
    db, clock = FakeDB(order()), Clock(at(6, 13, 15))
    queue.plan("order-1", 1, at(6, 13, 15))
    Worker(queue, Dialer(CallResult(status="answered", outcome="callback", callback_at=at(6, 19, 0))), db, now=clock).run_once()
    assert db.orders["order-1"]["status"] == "callback"
    assert queue.planned("order-1") == [(2, at(6, 19, 0))]


def test_callback_at_11pm_moves_to_9am(queue):
    db, clock = FakeDB(order()), Clock(at(6, 13, 15))
    queue.plan("order-1", 1, at(6, 13, 15))
    Worker(queue, Dialer(CallResult(status="answered", outcome="callback", callback_at=at(6, 23, 0))), db, now=clock).run_once()
    assert queue.planned("order-1") == [(2, at(7, 9, 0))]


def test_call_later_without_a_time_uses_retry_gap(queue):
    db, clock = FakeDB(order()), Clock(at(6, 15, 0))
    queue.plan("order-1", 1, at(6, 15, 0))
    Worker(queue, Dialer(CallResult(status="answered", outcome="callback")), db, now=clock).run_once()
    assert queue.planned("order-1") == [(2, at(6, 17, 0))]


# Task 4.6: never more than 5 calls at once
def test_twenty_orders_at_once_never_run_more_than_five_calls(queue):
    db = FakeDB(*[order(n) for n in range(20)])
    for n in range(20):
        queue.plan(f"order-{n}", 1, at(6, 10, 5))
    running = peak = 0
    lock = threading.Lock()

    def slow_call(order, attempt):
        nonlocal running, peak
        with lock:
            running += 1
            peak = max(peak, running)
        time.sleep(0.05)
        with lock:
            running -= 1
        return CallResult(status="answered", outcome="confirmed")

    handled = Worker(queue, slow_call, db, max_concurrent=5, now=Clock(at(6, 10, 5))).run_once()
    assert handled == 20
    assert peak == 5
    assert all(o["status"] == "confirmed" for o in db.orders.values())
