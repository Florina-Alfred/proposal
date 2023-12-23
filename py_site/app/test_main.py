from fastapi.testclient import TestClient
import time
import re
from .main import app

client = TestClient(app)


def test_working():
    response = client.get("/working")
    assert response.status_code == 200
    assert response.json() ==  {"working": "ok",
                                "language" : "python",
                                "time": time.strftime('%X %x %Z'),}
    
def test_metrics_app():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "test_guage" in response.text