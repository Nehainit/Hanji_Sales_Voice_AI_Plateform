"""Background worker: places due calls from the Redis queue and plans what comes next.

The phone call itself is made by a `dialer`. Phase 1 plugs in the real one (Exotel +
voice pipeline); tests use a fake. After each call the worker saves it, updates the
order, and then stops, plans a retry, or plans the callback the customer asked for.

Not here yet: the wallet balance check (Phase 4) and Shopify tags (shopify/tags.py).
"""
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from app.config import settings
from app.scheduler.planning import load_call_settings, to_ist
from app.scheduler.queue import IST, CallQueue
from app.scheduler.rules import next_allowed, next_retry_time
from app.voice.active_calls import ActiveCalls
from app.voice.flow_cod import CALLBACK, CANCELLED, CONFIRMED, NO_ANSWER

OPEN_STATUSES = {"pending", CALLBACK}  # orders that may still be called


@dataclass
class CallResult:
    status: str                       # answered | busy | not_answered | failed
    outcome: str | None = None        # confirmed | cancelled | callback (answered calls only)
    duration_seconds: int = 0
    cancel_reason: str | None = None
    new_address: str | None = None
    callback_at: datetime | None = None
    transcript: list[dict] = field(default_factory=list)
    error: str | None = None


Dialer = Callable[[dict, int], CallResult]  # (order row, attempt number) -> result


class Worker:
    def __init__(self, queue: CallQueue, dialer: Dialer, db, max_concurrent: int | None = None,
                 now: Callable[[], datetime] = lambda: datetime.now(IST), active_calls: ActiveCalls | None = None):
        self.queue = queue
        self.dialer = dialer
        self.db = db
        self.max_concurrent = max_concurrent or settings.max_concurrent_calls
        self.now = now
        self.active_calls = active_calls or ActiveCalls()

    def run_once(self) -> int:
        """Place every call that is due now, at most `max_concurrent` at a time. Returns how many."""
        handled = 0
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as pool:
            while jobs := self.queue.claim_due(self.now(), limit=self.max_concurrent):
                list(pool.map(lambda job: self._handle(*job), jobs))
                handled += len(jobs)
        return handled

    def run_forever(self, poll_seconds: float = 5) -> None:
        while True:
            self.run_once()
            time.sleep(poll_seconds)

    def _handle(self, order_id: str, attempt: int, scheduled_at: datetime) -> None:
        order = self.db.get_order(order_id)
        if not order or order["status"] not in OPEN_STATUSES:
            return  # confirmed, cancelled or gone since the call was planned
        phone = order["customer_phone"]
        if not self.active_calls.start(phone):
            self.queue.plan(order_id, attempt, self.now() + timedelta(minutes=2))
            return

        started = self.now()
        try:
            result = self.dialer(order, attempt)
        except Exception as e:  # a crash in the call counts as a failed call, not a lost order
            result = CallResult(status="failed", error=str(e))
        finally:
            self.active_calls.end(phone)
        ended = self.now()

        answered = result.status == "answered"
        self.db.save_call({
            "order_id": order_id, "attempt_no": attempt,
            "scheduled_at": scheduled_at.isoformat(), "started_at": started.isoformat(), "ended_at": ended.isoformat(),
            "duration_seconds": result.duration_seconds, "status": result.status, "error": result.error,
            "outcome": result.outcome if answered else NO_ANSWER,
            "cancel_reason": result.cancel_reason, "new_address": result.new_address,
            "callback_at": result.callback_at.isoformat() if result.callback_at else None,
            "transcript": result.transcript,
        })
        self._plan_next(order, attempt, result, ended)

    def _plan_next(self, order: dict, attempt: int, result: CallResult, ended: datetime) -> None:
        order_id = order["id"]
        s = load_call_settings(self.db, order["store_id"])
        answered = result.status == "answered"

        if answered and result.outcome in (CONFIRMED, CANCELLED):
            self.db.update_order(order_id, status=result.outcome)
            self.queue.cancel(order_id)
            return
        if answered and result.outcome == CALLBACK and result.callback_at:
            self.db.update_order(order_id, status=CALLBACK)
            self.queue.plan(order_id, attempt + 1, next_allowed(to_ist(result.callback_at), s))
            return

        # Not answered, busy, failed, or "call later" without a time: normal retry rules.
        retry_at = next_retry_time(ended, attempt, s)
        if retry_at is None:
            self.db.update_order(order_id, status=NO_ANSWER)
            return
        if answered:
            self.db.update_order(order_id, status=CALLBACK)
        self.queue.plan(order_id, attempt + 1, retry_at)
