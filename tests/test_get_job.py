from fastapi.testclient import TestClient
from unittest.mock import patch
from api.main import app

client = TestClient(app)


@patch("api.main.get_redis")
def test_get_job(mock_redis):
    mock_redis.return_value.hget.return_value = None

    response = client.get("/jobs/test-id")

    assert response.status_code == 404