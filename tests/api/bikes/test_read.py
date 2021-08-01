from typing import List

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import schemas, crud


def test_read_bikes(
    client: TestClient, bikes_with_model: List[schemas.BikeWithRelationships]
):
    response = client.get("/api/v1/bikes")
    assert response.status_code == 200
    bikes_test_list = response.json()
    assert len(bikes_test_list) == 3


def test_read_bikes_model_param(
    client: TestClient, bikes_with_model: List[schemas.BikeWithRelationships]
):
    params = {"model": "test bike model 1"}
    response = client.get("/api/v1/bikes", params=params)
    assert response.status_code == 200
    bikes_test_list = response.json()
    assert len(bikes_test_list) == 1
    assert bikes_test_list[0]["model"]["name"] == "test bike model 1"

    params = {"model": "test bike model 2"}
    response = client.get("/api/v1/bikes", params=params)
    assert response.status_code == 200
    bikes_test_list = response.json()
    assert len(bikes_test_list) == 2
    assert bikes_test_list[0]["model"]["name"] == "test bike model 2"


def test_read_bikes_is_deleted_param(
    client: TestClient,
    test_db: Session,
    bikes_with_model: List[schemas.BikeWithRelationships],
    deleted_bike_with_model: schemas.BikeWithRelationships,
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
    client: TestClient, bikes_with_model: List[schemas.BikeWithRelationships]
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
    bikes_with_model: List[schemas.BikeWithRelationships],
):
    bike_id = bikes_with_model[0].id
    response = client.get(f"/api/v1/bikes/{bike_id}")
    assert response.status_code == 200
    assert response.json() == bikes_with_model[0].dict()
