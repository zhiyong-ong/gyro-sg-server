from typing import Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import schemas, crud


def test_update_bike_model(
    client: TestClient,
    bike_model: schemas.BikeModel,
    test_db: Session,
    superuser_headers: Dict[str, str],
):
    update_data = {
        "name": "test model name 2",
    }
    response = client.patch(
        f"/api/v1/bike_models/{bike_model.id}",
        headers=superuser_headers,
        json=update_data,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "test model name 2"
    bike_model = crud.bike_model.get(test_db, id=bike_model.id)
    assert bike_model
    assert bike_model.name == "test model name 2"


def test_update_bike_model_missing_bike_model(
    client: TestClient,
    bike_model: schemas.BikeModel,
    test_db: Session,
    superuser_headers: Dict[str, str],
):
    update_data = {
        "name": "test model name 2",
    }
    response = client.patch(
        f"/api/v1/bike_models/999",
        headers=superuser_headers,
        json=update_data,
    )
    assert response.status_code == 404


def test_update_bike_model_basic_user(
    client: TestClient,
    bike_model: schemas.BikeModel,
    test_db: Session,
    user_headers: Dict[str, str],
):
    update_data = {
        "name": "test model name 2",
    }
    response = client.patch(
        f"/api/v1/bike_models/{bike_model.id}",
        headers=user_headers,
        json=update_data,
    )
    assert response.status_code == 400
