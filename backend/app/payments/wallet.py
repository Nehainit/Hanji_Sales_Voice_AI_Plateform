"""Wallet money rules: the balance and what each call costs.

Money is always whole paise (₹1 = 100 paise). The balance is never stored on its own:
it is the sum of the seller's wallet_transactions rows (+ recharges and credits,
- call charges), so every rupee can be traced.
"""
import math
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Prices:
    first_minute_paise: int = 300   # ₹3 for an answered call up to 1 minute
    extra_minute_paise: int = 200   # ₹2 for each extra minute or part of one


def balance_paise(amounts_paise: Iterable[int]) -> int:
    """Balance from a seller's wallet rows (positive and negative amounts)."""
    return sum(amounts_paise)


def call_charge_paise(duration_seconds: int, answered: bool, is_test: bool = False,
                      prices: Prices = Prices()) -> int:
    """What a finished call costs. Unanswered, busy, failed and test calls are free."""
    if not answered or is_test:
        return 0
    extra_minutes = max(0, math.ceil(duration_seconds / 60) - 1)
    return prices.first_minute_paise + extra_minutes * prices.extra_minute_paise
