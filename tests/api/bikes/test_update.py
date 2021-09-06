from typing import Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import schemas, crud


def test_update_bike_current_user(
    client: TestClient,
    bike_with_model_1: schemas.BikeResponse,
    test_db: Session,
    user_headers: Dict[str, str],
):
    update_data = {
        "color": "updated color",
    }
    response = client.patch(
        f"/api/v1/bikes/{bike_with_model_1.id}/me",
        headers=user_headers,
        json=update_data,
    )
    assert response.status_code == 200
    assert response.json()["color"] == "updated color"
    bike = crud.bike.get(test_db, id=bike_with_model_1.id)
    assert bike
    assert bike.color == "updated color"


def test_update_bike_current_user_bike_missing(
    client: TestClient,
    bike_with_model_1: schemas.BikeResponse,
    user_headers: Dict[str, str],
):
    update_data = {
        "color": "updated color",
    }
    response = client.patch(
        f"/api/v1/bikes/999/me", headers=user_headers, json=update_data
    )
    assert response.status_code == 404


def test_update_bike_current_user_no_user(
    client: TestClient,
    bike_with_model_1: schemas.BikeResponse,
):
    update_data = {
        "color": "updated color",
    }
    response = client.patch(
        f"/api/v1/bikes/{bike_with_model_1.id}/me", json=update_data
    )
    assert response.status_code == 401


def test_update_bike_current_user_incorrect_user(
    client: TestClient,
    bike_with_model_1: schemas.BikeResponse,
    other_user_headers: Dict[str, str],
):
    update_data = {
        "color": "updated color",
    }
    response = client.patch(
        f"/api/v1/bikes/{bike_with_model_1.id}/me",
        headers=other_user_headers,
        json=update_data,
    )
    assert response.status_code == 403


def test_update_bike(
    client: TestClient,
    bike_with_model_1: schemas.BikeResponse,
    test_db: Session,
    superuser_headers: Dict[str, str],
):
    update_data = {
        "color": "updated color",
    }
    response = client.patch(
        f"/api/v1/bikes/{bike_with_model_1.id}",
        headers=superuser_headers,
        json=update_data,
    )
    assert response.status_code == 200
    assert response.json()["color"] == "updated color"
    bike = crud.bike.get(test_db, id=bike_with_model_1.id)
    assert bike
    assert bike.color == "updated color"


def test_update_bike_basic_user(
    client: TestClient,
    bike_with_model_1: schemas.BikeResponse,
    user_headers: Dict[str, str],
):
    update_data = {
        "color": "updated color",
    }
    response = client.patch(
        f"/api/v1/bikes/{bike_with_model_1.id}", headers=user_headers, json=update_data
    )
    assert response.status_code == 400


def test_update_bike_missing_bike(
    client: TestClient,
    bike_with_model_1: schemas.BikeResponse,
    superuser_headers: Dict[str, str],
):
    update_data = {
        "color": "updated color",
    }
    response = client.patch(
        f"/api/v1/bikes/99", headers=superuser_headers, json=update_data
    )
    assert response.status_code == 404
