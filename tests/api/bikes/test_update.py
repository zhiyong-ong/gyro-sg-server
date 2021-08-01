from typing import Dict, Tuple

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import schemas


def test_update_bike_current_user(
    client: TestClient,
    test_db: Session,
    bike_with_model_1: schemas.BikeWithRelationships,
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


def test_update_bike_current_user_bike_missing(
    client: TestClient,
    test_db: Session,
    bike_with_model_1: schemas.BikeWithRelationships,
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
    test_db: Session,
    bike_with_model_1: schemas.BikeWithRelationships,
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
    test_db: Session,
    bike_with_model_1: schemas.BikeWithRelationships,
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
    test_db: Session,
    bike_with_model_1: schemas.BikeWithRelationships,
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


def test_update_bike_basic_user(
    client: TestClient,
    test_db: Session,
    bike_with_model_1: schemas.BikeWithRelationships,
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
    test_db: Session,
    bike_with_model_1: schemas.BikeWithRelationships,
    superuser_headers: Dict[str, str],
):
    update_data = {
        "color": "updated color",
    }
    response = client.patch(
        f"/api/v1/bikes/99", headers=superuser_headers, json=update_data
    )
    assert response.status_code == 404
