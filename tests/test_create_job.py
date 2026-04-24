from fastapi.testclient import TestClient
from unittest.mock import patch
from api.main import app

client = TestClient(app)


@patch("api.main.get_redis")
def test_create_job(mock_redis):
    mock_redis.return_value.lpush.return_value = True
    mock_redis.return_value.hset.return_value = True

    response = client.post("/jobs")

    assert response.status_code == 200
    assert "job_id" in response.json()