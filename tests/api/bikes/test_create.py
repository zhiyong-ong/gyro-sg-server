from typing import Dict

from starlette.testclient import TestClient

from app import schemas


def test_create_bike_current_user(
    client: TestClient,
    bike_model: schemas.BikeModel,
    user: schemas.User,
    user_headers: Dict[str, str],
):
    data = {
        "color": "test color 1",
        "licence_class_id": 1,
        "transmission_id": 1,
        "storage_box": True,
        "rate": 6.50,
        "rate_unit": "hour",
        "description": "test desc",
        "images": ["image1.jpg"],
        "model_id": bike_model.id,
    }
    response = client.post("/api/v1/bikes/me", headers=user_headers, json=data)
    assert response.status_code == 201
    assert response.json()["color"] == "test color 1"
    assert response.json()["licence_class"] == {'description': '400cc and above', 'name': 'Class 2'}
    assert response.json()["transmission"] == {'description': 'No clutch, no gears', 'name': 'Automatic'}
    assert response.json()["rate"] == 6.50
    assert response.json()["rate_unit"] == "hour"
    assert response.json()["description"] == "test desc"
    assert response.json()["images"] == ["image1.jpg"]
    assert response.json()["model"] == {'id': bike_model.id, 'is_deleted': False, 'name': bike_model.name}
    assert response.json()["model"]["name"] == bike_model.name
    assert response.json()["user"]["email"] == user.email


def test_create_bike_current_user_no_user(
    client: TestClient,
    bike_model: schemas.BikeModel,
    user: schemas.User,
):
    data = {
        "color": "test color 1",
        "licence_class_id": 1,
        "transmission_id": 1,
        "rate": "6",
        "rate_unit": "hour",
        "description": "test desc",
        "images": ["image1.jpg"],
        "model_id": bike_model.id,
    }
    response = client.post("/api/v1/bikes/me", json=data)
    assert response.status_code == 401
