"""Cleaning customer phone numbers before calling.

Only valid Indian mobile numbers are called: 10 digits starting with 6, 7, 8 or 9,
optionally written with +91, 91 or 0 in front and with spaces, dashes, dots or brackets.
Anything else is an invalid number and must not be called.
"""
import re

INVALID_NUMBER = "invalid_number"  # result recorded when a number can't be called

_SEPARATORS = re.compile(r"[\s\-.()]")
_MOBILE = re.compile(r"[6-9]\d{9}")


def normalize_mobile(raw: str | None) -> str | None:
    """Return the 10-digit mobile number, or None if it is not a valid Indian mobile."""
    if not raw:
        return None
    digits = _SEPARATORS.sub("", raw)
    if digits.startswith("+91"):
        digits = digits[3:]
    elif len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
    return digits if _MOBILE.fullmatch(digits) else None
