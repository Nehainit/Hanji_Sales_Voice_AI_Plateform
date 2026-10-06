"""Backend entry point. Run with: uvicorn app.main:app --reload"""
import redis
from fastapi import FastAPI

from app.config import settings
from app.orders import routes as order_routes

app = FastAPI(title="HaanJi backend")
app.include_router(order_routes.router)


def redis_reachable() -> bool:
    try:
        return bool(redis.Redis.from_url(settings.redis_url, socket_connect_timeout=2).ping())
    except redis.RedisError:
        return False


@app.get("/health")
def health():
    phase1 = settings.missing(
        "exotel_account_sid", "exotel_api_key", "exotel_api_token",
        "exotel_caller_id", "sarvam_api_key", "anthropic_api_key",
    )
    return {"ok": True, "phase1_keys_missing": phase1, "redis_reachable": redis_reachable()}


# Phase 1: app.include_router(voice_routes.router)   (app/voice/routes.py)
# Phase 2: app.include_router(shopify_webhooks.router) (app/shopify/webhooks.py)
# Phase 4: app.include_router(razorpay.router)        (app/payments/razorpay.py)
