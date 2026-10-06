import sys
import uuid
from pathlib import Path

import pytest
import redis

# Let tests import the `app` package when pytest runs from backend/.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.scheduler.queue import CallQueue  # noqa: E402


@pytest.fixture
def queue():
    """A CallQueue on local Redis (database 15) with its own key prefix, cleaned up after."""
    client = redis.Redis(db=15, decode_responses=True)
    try:
        client.ping()
    except redis.RedisError:
        pytest.skip("Redis not running")
    prefix = f"test-{uuid.uuid4().hex[:8]}"
    yield CallQueue(client, prefix=prefix)
    keys = list(client.scan_iter(f"{prefix}:*"))
    if keys:
        client.delete(*keys)
