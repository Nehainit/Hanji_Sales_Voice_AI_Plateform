"""Reads settings and API keys from the project's .env file."""
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


@dataclass(frozen=True)
class Settings:
    # Phase 1: voice
    exotel_account_sid: str = os.getenv("EXOTEL_ACCOUNT_SID", "")
    exotel_api_key: str = os.getenv("EXOTEL_API_KEY", "")
    exotel_api_token: str = os.getenv("EXOTEL_API_TOKEN", "")
    exotel_subdomain: str = os.getenv("EXOTEL_SUBDOMAIN", "api.exotel.com")
    exotel_caller_id: str = os.getenv("EXOTEL_CALLER_ID", "")
    sarvam_api_key: str = os.getenv("SARVAM_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    claude_model: str = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001")
    public_base_url: str = os.getenv("PUBLIC_BASE_URL", "")

    # Phase 2: orders, queue, database
    shopify_api_key: str = os.getenv("SHOPIFY_API_KEY", "")
    shopify_api_secret: str = os.getenv("SHOPIFY_API_SECRET", "")
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    max_concurrent_calls: int = int(os.getenv("MAX_CONCURRENT_CALLS", "5"))

    # Phase 4: payments
    razorpay_key_id: str = os.getenv("RAZORPAY_KEY_ID", "")
    razorpay_key_secret: str = os.getenv("RAZORPAY_KEY_SECRET", "")

    def missing(self, *names: str) -> list[str]:
        """Names of the given settings that are still empty."""
        return [n for n in names if not getattr(self, n)]


settings = Settings()
