from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_all_trains():
    response = client.get("/api/v1/trains")
    assert response.status_code == 200
