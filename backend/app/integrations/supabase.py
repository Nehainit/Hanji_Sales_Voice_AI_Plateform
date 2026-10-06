"""Database access (Supabase / Postgres) through Supabase's REST API.

Uses the service role key, so it bypasses row level security: backend only, never
send this key to a browser. Tables are defined in database/schema.sql.
"""
import httpx

from app.config import settings


def _rest() -> httpx.Client:
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
    return httpx.Client(
        base_url=f"{settings.supabase_url}/rest/v1",
        headers={"apikey": settings.supabase_service_role_key, "Content-Type": "application/json"},
        timeout=20,
    )


def _one(response: httpx.Response) -> dict | None:
    response.raise_for_status()
    rows = response.json()
    return rows[0] if rows else None


def get_store(store_id: str) -> dict | None:
    with _rest() as db:
        response = db.get("/stores", params={"id": f"eq.{store_id}", "select": "*"})
        if response.status_code == 400:  # not a valid id
            return None
        return _one(response)


def get_call_settings(store_id: str) -> dict | None:
    """The calling settings of the seller who owns this store, or None for defaults."""
    store = get_store(store_id)
    if not store:
        return None
    with _rest() as db:
        return _one(db.get("/call_settings", params={"seller_id": f"eq.{store['seller_id']}", "select": "*"}))


def get_order(order_id: str) -> dict | None:
    with _rest() as db:
        return _one(db.get("/orders", params={"id": f"eq.{order_id}", "select": "*"}))


def save_order(order: dict) -> tuple[dict, bool]:
    """Save a new order. If the store already sent this order, keep the first copy.

    Returns (order row, created) where created is False for a repeat.
    """
    with _rest() as db:
        created = _one(db.post(
            "/orders",
            params={"on_conflict": "store_id,external_order_id"},
            headers={"Prefer": "resolution=ignore-duplicates,return=representation"},
            json=order,
        ))
        if created:
            return created, True
        existing = _one(db.get("/orders", params={
            "store_id": f"eq.{order['store_id']}",
            "external_order_id": f"eq.{order['external_order_id']}",
            "select": "*",
        }))
        return existing, False


def update_order(order_id: str, **fields) -> dict | None:
    """Change fields on an order, e.g. update_order(id, status="confirmed")."""
    with _rest() as db:
        return _one(db.patch(
            "/orders",
            params={"id": f"eq.{order_id}"},
            headers={"Prefer": "return=representation"},
            json=fields,
        ))


def save_call(call: dict) -> dict:
    """Save a call attempt (planned or finished) for an order."""
    with _rest() as db:
        return _one(db.post("/calls", headers={"Prefer": "return=representation"}, json=call))
