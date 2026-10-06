from datetime import datetime, timedelta, timezone

from app.scheduler.rules import CallSettings, first_call_time, next_retry_time

IST = timezone(timedelta(hours=5, minutes=30))
S = CallSettings()


def at(day, hour, minute=0):
    return datetime(2026, 10, day, hour, minute, tzinfo=IST)


def test_first_call_after_delay_inside_window():
    assert first_call_time(at(6, 10, 0), S) == at(6, 10, 5)


def test_late_night_order_waits_for_next_morning():
    assert first_call_time(at(6, 20, 58), S) == at(7, 9, 0)


def test_early_morning_order_waits_for_window_start():
    assert first_call_time(at(6, 2, 0), S) == at(6, 9, 0)


def test_retry_after_gap():
    assert next_retry_time(at(6, 12, 0), attempts_made=1, s=S) == at(6, 14, 0)


def test_retry_that_lands_after_hours_moves_to_next_morning():
    assert next_retry_time(at(6, 20, 0), attempts_made=2, s=S) == at(7, 9, 0)


def test_no_retry_after_max_attempts():
    assert next_retry_time(at(6, 12, 0), attempts_made=3, s=S) is None
