from fastapi.testclient import TestClient
import time
from .main import app

client = TestClient(app)


def test_api():
    response = client.get("/api")
    assert response.status_code == 200


def test_working():
    response = client.get("/working")
    assert response.status_code == 200
    assert response.json() == {
        "working": "ok",
        "language": "python",
        "time": time.strftime("%X %x %Z"),
    }


def test_metrics_app():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "test_guage" in response.text
