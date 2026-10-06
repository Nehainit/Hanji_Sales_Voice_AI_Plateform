from fastapi.testclient import TestClient

import app.main as main


def test_health_reports_redis_down(monkeypatch):
    monkeypatch.setattr(main, "redis_reachable", lambda: False)
    body = TestClient(main.app).get("/health").json()
    assert body["ok"] is True
    assert body["redis_reachable"] is False


def test_redis_reachable_false_when_nothing_listens(monkeypatch):
    class FakeSettings:
        redis_url = "redis://localhost:1/0"  # nothing listens on port 1
    monkeypatch.setattr(main, "settings", FakeSettings())
    assert main.redis_reachable() is False
