from typing import List

import pytest
from sqlalchemy.orm import Session

from app import crud, schemas
from app.models.bike import Bike, BikeModel


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


@pytest.fixture
def bike_model_deleted(test_db: Session) -> schemas.BikeModel:
    bike_model_test_model = BikeModel(
        name="test bike model 2",
        is_deleted=True,
    )
    bike_model_test = crud.bike_model.create_db_model(
        test_db, db_model_in=bike_model_test_model
    )
    assert bike_model_test
    bike_model_test_schema = schemas.BikeModel.from_orm(bike_model_test)
    assert bike_model_test_schema
    return bike_model_test_schema
