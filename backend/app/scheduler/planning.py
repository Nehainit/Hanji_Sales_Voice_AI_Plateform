"""Turning an order into planned calls, using the seller's calling settings."""
from datetime import datetime, time, timedelta

from app.scheduler.queue import IST, CallQueue
from app.scheduler.rules import CallSettings, first_call_time


def to_ist(value: str | datetime) -> datetime:
    """Database timestamps (ISO text) or datetimes → Indian time."""
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    return value.astimezone(IST)


def call_settings_from_row(row: dict | None) -> CallSettings:
    """A call_settings table row → CallSettings. No row means the defaults."""
    if not row:
        return CallSettings()
    return CallSettings(
        delay_minutes=row["delay_minutes"],
        window_start=time.fromisoformat(row["window_start"]),
        window_end=time.fromisoformat(row["window_end"]),
        max_attempts=row["max_attempts"],
        retry_gap=timedelta(minutes=row["retry_gap_minutes"]),
    )


def load_call_settings(db, store_id: str) -> CallSettings:
    return call_settings_from_row(db.get_call_settings(store_id))


def plan_first_call(queue: CallQueue, order: dict, settings: CallSettings) -> datetime:
    """Plan attempt 1 for a new order. Returns when it will happen."""
    at = first_call_time(to_ist(order["created_at"]), settings)
    queue.plan(order["id"], 1, at)
    return at
