import os

os.environ["MODEL_DIR"] = "artifacts"

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402

client = TestClient(app)


def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data


def test_predict_error_shape():
    resp = client.post("/predict", json={"age": 0.1})
    assert resp.status_code in (400, 422)
