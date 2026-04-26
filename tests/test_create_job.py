from fastapi.testclient import TestClient
from unittest.mock import patch
from api.main import app

client = TestClient(app)


@patch("api.main.get_redis")
def test_create_job(mock_redis):
    mock = mock_redis.return_value
    mock.lpush.return_value = True
    mock.hset.return_value = True

    res = client.post("/jobs")
    assert res.status_code == 200