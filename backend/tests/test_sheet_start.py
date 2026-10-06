"""Task 3.7: sheet calls start only when the seller presses "Start calling".

Uses the real Supabase project and local Redis; skipped when either is missing.
"""
import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.integrations.supabase import _rest
from app.main import app
from app.scheduler.queue import get_queue
from test_sheet import as_csv, fifty_rows_with_two_bad

pytestmark = pytest.mark.skipif(
    not (settings.supabase_url and settings.supabase_service_role_key), reason="Supabase not configured"
)


@pytest.fixture
def client(queue):
    app.dependency_overrides[get_queue] = lambda: queue
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def store():
    with _rest() as db:
        seller = db.post("/sellers", headers={"Prefer": "return=representation"},
                         json={"brand_name": "pytest — sheet start"}).json()[0]
        store = db.post("/stores", headers={"Prefer": "return=representation"},
                        json={"seller_id": seller["id"], "platform": "sheet"}).json()[0]
    yield store
    with _rest() as db:
        db.delete("/sellers", params={"id": f"eq.{seller['id']}"}).raise_for_status()


def orders_in_store(store_id):
    with _rest() as db:
        return db.get("/orders", params={"store_id": f"eq.{store_id}", "select": "id"}).json()


def upload(name="orders.csv"):
    return {"file": (name, as_csv(fifty_rows_with_two_bad()), "text/csv")}


def test_checking_a_sheet_saves_nothing_and_plans_no_calls(client, queue, store):
    res = client.post("/orders/sheet/check", files=upload())
    assert res.json()["ready"] == 48
    assert orders_in_store(store["id"]) == []
    assert queue.size() == 0


def test_start_calling_saves_orders_and_plans_their_first_calls(client, queue, store):
    res = client.post("/orders/sheet/start", files=upload(), data={"store_id": store["id"]})
    assert res.status_code == 200
    body = res.json()
    assert (body["saved"], body["calls_planned"]) == (48, 48)
    assert body["problems_text"] == "Row 5: phone missing, Row 9: amount missing"
    assert len(orders_in_store(store["id"])) == 48
    assert queue.size() == 48


def test_pressing_start_twice_does_not_plan_calls_twice(client, queue, store):
    client.post("/orders/sheet/start", files=upload(), data={"store_id": store["id"]})
    body = client.post("/orders/sheet/start", files=upload(), data={"store_id": store["id"]}).json()
    assert (body["saved"], body["already_saved"], body["calls_planned"]) == (0, 48, 0)
    assert queue.size() == 48


def test_unknown_store_is_refused(client, queue):
    res = client.post("/orders/sheet/start", files=upload(), data={"store_id": "not-a-store"})
    assert res.status_code == 404
    assert queue.size() == 0
