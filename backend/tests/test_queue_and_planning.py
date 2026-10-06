from datetime import datetime, time, timedelta

from app.scheduler.planning import call_settings_from_row, plan_first_call
from app.scheduler.queue import IST
from app.scheduler.rules import CallSettings


def at(day, hour, minute=0):
    return datetime(2026, 10, day, hour, minute, tzinfo=IST)


# Task 4.1 / spec scheduler/call-scheduling
def test_late_night_order_is_planned_for_9am_next_day(queue):
    order = {"id": "order-late", "created_at": "2026-10-06T15:28:00+00:00"}  # 8:58 PM IST
    planned_at = plan_first_call(queue, order, CallSettings())
    assert planned_at == at(7, 9, 0)
    assert queue.planned("order-late") == [(1, at(7, 9, 0))]


def test_daytime_order_is_planned_after_5_minutes(queue):
    order = {"id": "order-day", "created_at": at(6, 10, 0).isoformat()}
    assert plan_first_call(queue, order, CallSettings()) == at(6, 10, 5)


def test_seller_settings_are_used(queue):
    row = {"delay_minutes": 15, "window_start": "10:00:00", "window_end": "20:00:00",
           "max_attempts": 2, "retry_gap_minutes": 60}
    s = call_settings_from_row(row)
    assert (s.window_start, s.window_end, s.max_attempts, s.retry_gap) == (time(10), time(20), 2, timedelta(hours=1))
    order = {"id": "order-930", "created_at": at(6, 9, 30).isoformat()}
    assert plan_first_call(queue, order, s) == at(6, 10, 0)


def test_no_settings_row_means_defaults():
    assert call_settings_from_row(None) == CallSettings()


# Queue behaviour
def test_same_call_cannot_be_planned_twice(queue):
    assert queue.plan("o1", 1, at(6, 10, 5)) is True
    assert queue.plan("o1", 1, at(6, 11, 0)) is False
    assert queue.planned("o1") == [(1, at(6, 10, 5))]


def test_only_due_calls_are_claimed_and_only_once(queue):
    queue.plan("o1", 1, at(6, 10, 5))
    queue.plan("o2", 1, at(6, 12, 0))
    assert queue.claim_due(at(6, 11, 0)) == [("o1", 1, at(6, 10, 5))]
    assert queue.claim_due(at(6, 11, 0)) == []
    assert queue.size() == 1


def test_cancel_drops_all_planned_calls_for_an_order(queue):
    queue.plan("o1", 1, at(6, 10, 5))
    queue.plan("o1", 2, at(6, 12, 5))
    queue.plan("o2", 1, at(6, 10, 5))
    assert queue.cancel("o1") == 2
    assert queue.planned("o1") == []
    assert queue.size() == 1
