from typing import Dict

from starlette.testclient import TestClient

from app import schemas


def test_create_bike_model(
    client: TestClient,
    superuser_headers: Dict[str, str],
):
    data = {
        "name": "test model",
    }
    response = client.post("/api/v1/bike_models", headers=superuser_headers, json=data)
    assert response.status_code == 201
    assert response.json()["name"] == "test model"
    assert response.json()["is_deleted"] is False


def test_create_bike_model_missing_name(
    client: TestClient,
    superuser_headers: Dict[str, str],
):
    data = {
        "is_deleted": False,
    }
    response = client.post("/api/v1/bike_models", headers=superuser_headers, json=data)
    assert response.status_code == 422


def test_create_bike_model_basic_user(
    client: TestClient,
    user_headers: Dict[str, str],
):
    data = {
        "name": "test model",
    }
    response = client.post("/api/v1/bike_models", headers=user_headers, json=data)
    assert response.status_code == 400
