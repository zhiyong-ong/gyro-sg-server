from typing import List

from starlette.testclient import TestClient

from app import schemas


def test_read_bike_models(
    client: TestClient,
    bike_model: schemas.BikeModel,
    bike_model_deleted: schemas.BikeModel,
):
    response = client.get("/api/v1/bike_models")
    assert response.status_code == 200
    bikes_test_list = response.json()
    assert len(bikes_test_list) == 2


def test_read_bike_model_is_deleted_param(
    client: TestClient,
    bike_model: schemas.BikeModel,
    bike_model_deleted: schemas.BikeModel,
):
    params = {"is_deleted": False}
    response = client.get("/api/v1/bike_models", params=params)
    assert response.status_code == 200
    bike_models_list = response.json()
    assert len(bike_models_list) == 1

    params = {"is_deleted": True}
    response = client.get("/api/v1/bike_models", params=params)
    assert response.status_code == 200
    bike_models_list = response.json()
    assert len(bike_models_list) == 1


def test_read_bike_models_offset_limit_param(
    client: TestClient,
    bike_model: schemas.BikeModel,
    bike_model_deleted: schemas.BikeModel,
):
    params = {"limit": 1}
    response = client.get("/api/v1/bike_models", params=params)
    assert response.status_code == 200
    bike_models_list = response.json()
    assert len(bike_models_list) == 1

    params = {"offset": 1}
    response = client.get("/api/v1/bike_models", params=params)
    assert response.status_code == 200
    bike_models_list = response.json()
    assert len(bike_models_list) == 1

    params = {"limit": 1, "offset": 1}
    response = client.get("/api/v1/bike_models", params=params)
    assert response.status_code == 200
    bike_models_list = response.json()
    assert len(bike_models_list) == 1


def test_read_bike_model(
    client: TestClient,
    bike_model: schemas.BikeModel,
):
    response = client.get(f"/api/v1/bike_models/{bike_model.id}")
    assert response.status_code == 200
    assert response.json() == bike_model.dict()
