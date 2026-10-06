"""Talks to the real Supabase project in .env. Skipped when Supabase isn't configured.

Creates a throwaway seller, then deletes it (which deletes its store, orders and calls).
"""
from datetime import datetime, timedelta, timezone

import pytest

from app.config import settings
from app.integrations.supabase import _rest, get_order, save_call, save_order, update_order

pytestmark = pytest.mark.skipif(
    not (settings.supabase_url and settings.supabase_service_role_key), reason="Supabase not configured"
)
IST = timezone(timedelta(hours=5, minutes=30))


@pytest.fixture
def store():
    with _rest() as db:
        seller = db.post("/sellers", headers={"Prefer": "return=representation"},
                         json={"brand_name": "pytest — Kesar Kurtis"}).json()[0]
        store = db.post("/stores", headers={"Prefer": "return=representation"},
                        json={"seller_id": seller["id"], "platform": "sheet"}).json()[0]
    yield store
    with _rest() as db:
        db.delete("/sellers", params={"id": f"eq.{seller['id']}"}).raise_for_status()


def sample_order(store_id):
    return {
        "store_id": store_id, "external_order_id": "KK2148", "customer_name": "Priya Sharma",
        "customer_phone": "9829041122", "amount_paise": 129900,
        "product_summary": "Cotton Anarkali Kurti", "address": "B-24, Malviya Nagar, Jaipur 302017",
    }


# Task 2.1: save a sample order and read it back
def test_save_order_and_read_it_back(store):
    saved, created = save_order(sample_order(store["id"]))
    assert created is True
    read = get_order(saved["id"])
    assert read["customer_name"] == "Priya Sharma"
    assert read["amount_paise"] == 129900
    assert read["status"] == "pending"


def test_same_order_twice_keeps_one_copy(store):
    first, _ = save_order(sample_order(store["id"]))
    second, created = save_order(sample_order(store["id"]))
    assert created is False
    assert second["id"] == first["id"]


def test_update_order_status(store):
    saved, _ = save_order(sample_order(store["id"]))
    assert update_order(saved["id"], status="confirmed")["status"] == "confirmed"
    assert get_order(saved["id"])["status"] == "confirmed"


def test_save_call_for_order(store):
    saved, _ = save_order(sample_order(store["id"]))
    call = save_call({"order_id": saved["id"], "attempt_no": 1,
                      "scheduled_at": datetime(2026, 10, 6, 10, 5, tzinfo=IST).isoformat(),
                      "status": "failed", "error": "network down", "outcome": "no_answer", "transcript": []})
    assert call["order_id"] == saved["id"]
    assert (call["attempt_no"], call["status"], call["error"]) == (1, "failed", "network down")
