"""Calling rules: when a call may go out and when to retry.

Pure functions with no I/O so they are easy to test. Pass timezone-aware
datetimes in Asia/Kolkata so the calling window means Indian local time.
"""
from dataclasses import dataclass
from datetime import datetime, time, timedelta


@dataclass(frozen=True)
class CallSettings:
    delay_minutes: int = 5               # wait after the order is placed
    window_start: time = time(9, 0)      # no calls before this
    window_end: time = time(21, 0)       # no calls at or after this
    max_attempts: int = 3
    retry_gap: timedelta = timedelta(hours=2)


def within_window(at: datetime, s: CallSettings) -> bool:
    return s.window_start <= at.time() < s.window_end


def next_allowed(at: datetime, s: CallSettings) -> datetime:
    """Earliest moment at or after `at` that falls inside the calling window."""
    if within_window(at, s):
        return at
    start_today = at.replace(
        hour=s.window_start.hour, minute=s.window_start.minute, second=0, microsecond=0
    )
    if at.time() < s.window_start:
        return start_today
    return start_today + timedelta(days=1)


def first_call_time(order_placed_at: datetime, s: CallSettings) -> datetime:
    return next_allowed(order_placed_at + timedelta(minutes=s.delay_minutes), s)


def next_retry_time(last_attempt_at: datetime, attempts_made: int, s: CallSettings) -> datetime | None:
    """When to try again after an unanswered call, or None when attempts are used up."""
    if attempts_made >= s.max_attempts:
        return None
    return next_allowed(last_attempt_at + s.retry_gap, s)
