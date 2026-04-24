from fastapi.testclient import TestClient
import main

class FakeRedis:
    def hget(self, *a): return None
    def ping(self): return True

def test_get_job_not_found(monkeypatch):
    monkeypatch.setattr(main, "get_redis", lambda: FakeRedis())
    client = TestClient(main.app)

    r = client.get("/jobs/123")
    assert r.status_code == 404