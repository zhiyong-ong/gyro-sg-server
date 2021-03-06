from typing import List

from starlette.testclient import TestClient

from app import schemas


def test_read_bikes(
    client: TestClient,
    bikes_with_models: List[schemas.BikeResponse],
    deleted_bike_with_model: schemas.BikeResponse,
):
    response = client.get("/api/v1/bikes")
    assert response.status_code == 200
    bikes_test_list = response.json()
    assert len(bikes_test_list) == 4


def test_read_bikes_model_name_param(
    client: TestClient, bikes_with_models: List[schemas.BikeResponse]
):
    params = {"model_name": bikes_with_models[0].model.name}
    response = client.get("/api/v1/bikes", params=params)
    assert response.status_code == 200
    bikes_test_list = response.json()
    assert len(bikes_test_list) == 1
    assert bikes_test_list[0]["model"]["name"] == bikes_with_models[0].model.name

    params = {"model_name": bikes_with_models[1].model.name}
    response = client.get("/api/v1/bikes", params=params)
    assert response.status_code == 200
    bikes_test_list = response.json()
    assert len(bikes_test_list) == 2
    assert bikes_test_list[0]["model"]["name"] == bikes_with_models[1].model.name


def test_read_bikes_is_deleted_param(
    client: TestClient,
    bikes_with_models: List[schemas.BikeResponse],
    deleted_bike_with_model: schemas.BikeResponse,
):
    params = {"is_deleted": False}
    response = client.get("/api/v1/bikes", params=params)
    assert response.status_code == 200
    bikes_test_list = response.json()
    assert len(bikes_test_list) == 3

    params = {"is_deleted": True}
    response = client.get("/api/v1/bikes", params=params)
    assert response.status_code == 200
    bikes_test_list = response.json()
    assert len(bikes_test_list) == 1


def test_read_bikes_offset_limit_param(
    client: TestClient, bikes_with_models: List[schemas.BikeResponse]
):
    params = {"limit": 1}
    response = client.get("/api/v1/bikes", params=params)
    assert response.status_code == 200
    bikes_test_list = response.json()
    assert len(bikes_test_list) == 1

    params = {"offset": 2}
    response = client.get("/api/v1/bikes", params=params)
    assert response.status_code == 200
    bikes_test_list = response.json()
    assert len(bikes_test_list) == 1

    params = {"limit": 1, "offset": 1}
    response = client.get("/api/v1/bikes", params=params)
    assert response.status_code == 200
    bikes_test_list = response.json()
    assert len(bikes_test_list) == 1


def test_read_bike(
    client: TestClient,
    bikes_with_models: List[schemas.BikeResponse],
):
    bike_id = bikes_with_models[0].id
    response = client.get(f"/api/v1/bikes/{bike_id}")
    assert response.status_code == 200
    assert response.json() == bikes_with_models[0].dict()
