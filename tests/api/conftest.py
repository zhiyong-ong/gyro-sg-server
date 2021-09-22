from typing import Dict, Tuple

import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import schemas, crud
from app.models import BikeModel, Transmission
from app.schemas import UserCreate
from tests.utils.user import user_authentication_headers

password = "password"


@pytest.fixture
def user(client: TestClient, test_db: Session) -> schemas.UserWithId:
    email = "test_user@example.com"
    first_name = "first"
    last_name = "last"
    user_in_create = UserCreate(
        email=email, password=password, first_name=first_name, last_name=last_name
    )
    user_model = crud.user.create(test_db, obj_in=user_in_create)
    return schemas.UserWithId.from_orm(user_model)


@pytest.fixture
def user_headers(
    client: TestClient, test_db: Session, user: schemas.UserWithId
) -> Dict[str, str]:
    headers = user_authentication_headers(
        client=client, email=user.email, password=password
    )
    return headers


@pytest.fixture
def other_user(client: TestClient, test_db: Session) -> schemas.UserWithId:
    email = "test_user_2@example.com"
    first_name = "first"
    last_name = "last"
    user_in_create = UserCreate(
        email=email, password=password, first_name=first_name, last_name=last_name
    )
    user_model = crud.user.create(test_db, obj_in=user_in_create)
    return schemas.UserWithId.from_orm(user_model)


@pytest.fixture
def other_user_headers(
    client: TestClient, test_db: Session, other_user: schemas.UserWithId
) -> Dict[str, str]:
    headers = user_authentication_headers(
        client=client, email=other_user.email, password=password
    )
    return headers


@pytest.fixture
def bike_model(test_db: Session) -> schemas.BikeModel:
    bike_model_test_model = BikeModel(
        name="test bike model 1",
    )
    bike_model_test = crud.bike_model.create_db_model(
        test_db, db_model_in=bike_model_test_model
    )
    assert bike_model_test
    bike_model_test_schema = schemas.BikeModel.from_orm(bike_model_test)
    assert bike_model_test_schema
    return bike_model_test_schema
