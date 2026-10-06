"""Tracks which phone numbers are on a call right now, so a number is never called twice at once.

Phase 1 runs as a single process, so an in-memory set is enough. Phase 2 moves this to
Redis when several workers place calls.
"""
import threading


class ActiveCalls:
    def __init__(self):
        self._numbers: set[str] = set()
        self._lock = threading.Lock()

    def start(self, number: str) -> bool:
        """Mark the number as on a call. False means it already is: don't place the new call."""
        with self._lock:
            if number in self._numbers:
                return False
            self._numbers.add(number)
            return True

    def end(self, number: str) -> None:
        with self._lock:
            self._numbers.discard(number)

    def __contains__(self, number: str) -> bool:
        with self._lock:
            return number in self._numbers


active_calls = ActiveCalls()
