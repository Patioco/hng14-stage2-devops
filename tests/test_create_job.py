from fastapi.testclient import TestClient
from api.main import app

class FakeRedis:
    def lpush(self, *a): pass
    def hset(self, *a, **k): pass
    def ping(self): return True

def test_create_job(monkeypatch):
    monkeypatch.setattr(main, "get_redis", lambda: FakeRedis())
    client = TestClient(main.app)

    r = client.post("/jobs")
    assert r.status_code == 200
    assert "job_id" in r.json()