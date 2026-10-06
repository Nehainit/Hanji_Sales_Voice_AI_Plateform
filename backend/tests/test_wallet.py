from app.payments.wallet import Prices, balance_paise, call_charge_paise


# Task 2.1: balance is the sum of the wallet rows
def test_balance_after_credit_and_two_calls():
    rows = [15000, -300, -500]  # +₹150 free credit, −₹3 call, −₹5 call
    assert balance_paise(rows) == 14200  # ₹142


def test_empty_wallet():
    assert balance_paise([]) == 0


# Task 2.3 / spec payments/seller-wallet: Only answered calls are charged
def test_short_answered_call_costs_3():
    assert call_charge_paise(42, answered=True) == 300


def test_long_answered_call_costs_5():
    assert call_charge_paise(80, answered=True) == 500  # 1 min 20 s


def test_unanswered_call_is_free():
    assert call_charge_paise(0, answered=False) == 0


def test_test_call_is_free():
    assert call_charge_paise(42, answered=True, is_test=True) == 0


# Minute boundaries: "each extra minute or part of a minute"
def test_exactly_one_minute_costs_3():
    assert call_charge_paise(60, answered=True) == 300


def test_one_second_over_a_minute_costs_5():
    assert call_charge_paise(61, answered=True) == 500


def test_three_minute_call_costs_7():
    assert call_charge_paise(180, answered=True) == 700


def test_new_prices_apply():
    assert call_charge_paise(80, answered=True, prices=Prices(first_minute_paise=400, extra_minute_paise=250)) == 650
