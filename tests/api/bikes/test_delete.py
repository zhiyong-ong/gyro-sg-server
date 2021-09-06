from typing import Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import schemas, crud


def test_delete_bike_current_user(
    client: TestClient,
    test_db: Session,
    bike_with_model_1: schemas.BikeResponse,
    user_headers: Dict[str, str],
):
    response = client.delete(
        f"/api/v1/bikes/{bike_with_model_1.id}/me", headers=user_headers
    )
    assert response.status_code == 200
    bike = crud.bike.get(test_db, id=bike_with_model_1.id)
    assert bike
    assert bike.is_deleted is True


def test_delete_bike_current_user_bike_missing(
    client: TestClient,
    bike_with_model_1: schemas.BikeResponse,
    user_headers: Dict[str, str],
):
    response = client.delete(f"/api/v1/bikes/999/me", headers=user_headers)
    assert response.status_code == 404


def test_delete_bike_current_user_no_user(
    client: TestClient,
    bike_with_model_1: schemas.BikeResponse,
):
    response = client.delete(
        f"/api/v1/bikes/{bike_with_model_1.id}/me",
    )
    assert response.status_code == 401


def test_delete_bike_current_user_incorrect_user(
    client: TestClient,
    bike_with_model_1: schemas.BikeResponse,
    other_user_headers: Dict[str, str],
):
    response = client.delete(
        f"/api/v1/bikes/{bike_with_model_1.id}/me", headers=other_user_headers
    )
    assert response.status_code == 403


def test_delete_bike(
    client: TestClient,
    test_db: Session,
    bike_with_model_1: schemas.BikeResponse,
    superuser_headers: Dict[str, str],
):
    response = client.delete(
        f"/api/v1/bikes/{bike_with_model_1.id}", headers=superuser_headers
    )
    assert response.status_code == 200
    bike = crud.bike.get(test_db, id=bike_with_model_1.id)
    assert bike
    assert bike.is_deleted is True


def test_delete_bike_basic_user(
    client: TestClient,
    bike_with_model_1: schemas.BikeResponse,
    user_headers: Dict[str, str],
):
    response = client.delete(
        f"/api/v1/bikes/{bike_with_model_1.id}", headers=user_headers
    )
    assert response.status_code == 400


def test_delete_bike_missing_bike(
    client: TestClient,
    bike_with_model_1: schemas.BikeResponse,
    superuser_headers: Dict[str, str],
):
    response = client.delete(f"/api/v1/bikes/99", headers=superuser_headers)
    assert response.status_code == 404
