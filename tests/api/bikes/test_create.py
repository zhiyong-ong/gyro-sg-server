from typing import Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import schemas


def test_create_bike_current_user(
    client: TestClient,
    test_db: Session,
    bike_model_1: schemas.BikeModel,
    user: schemas.User,
    user_headers,
):
    data = {
        "color": "test color 1",
        "required_licence": "2A",
        "transmission": "manual",
        "rate": "6",
        "rate_unit": "hour",
        "description": "test desc",
        "images": ["image1.jpg"],
        "model_id": bike_model_1.id,
    }
    response = client.post("/api/v1/bikes/me", headers=user_headers, json=data)
    assert response.status_code == 201
    assert response.json()["color"] == "test color 1"
    assert response.json()["required_licence"] == "2A"
    assert response.json()["transmission"] == "manual"
    assert response.json()["rate"] == "6"
    assert response.json()["rate_unit"] == "hour"
    assert response.json()["description"] == "test desc"
    assert response.json()["images"] == ["image1.jpg"]
    assert response.json()["model_id"] == bike_model_1.id
    assert response.json()["model"]["name"] == bike_model_1.name
    assert response.json()["user"]["email"] == user.email


def test_create_bike_current_user_no_user(
    client: TestClient,
    test_db: Session,
    bike_model_1: schemas.BikeModel,
    user: schemas.User,
):
    data = {
        "color": "test color 1",
        "required_licence": "2A",
        "transmission": "manual",
        "rate": "6",
        "rate_unit": "hour",
        "description": "test desc",
        "images": ["image1.jpg"],
        "model_id": bike_model_1.id,
    }
    response = client.post("/api/v1/bikes/me", json=data)
    assert response.status_code == 401
