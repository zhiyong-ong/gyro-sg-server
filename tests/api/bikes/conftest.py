from typing import List

import pytest
from sqlalchemy.orm import Session

from app import crud, schemas
from app.models.bike import Bike, BikeModel


@pytest.fixture
def bike_model_1(test_db: Session):
	bike_model_test_model = BikeModel(
		name="test bike model 1",
	)
	bike_model_test = crud.bike_model.create_db_model(test_db, db_model_in=bike_model_test_model)
	assert bike_model_test
	bike_model_test_schema = schemas.BikeModel.from_orm(bike_model_test)
	assert bike_model_test_schema
	return bike_model_test_schema

@pytest.fixture
def bike_model_2(test_db: Session):
	bike_model_test_model = BikeModel(
		name="test bike model 2",
	)
	bike_model_test = crud.bike_model.create_db_model(test_db, db_model_in=bike_model_test_model)
	assert bike_model_test
	bike_model_test_schema = schemas.BikeModel.from_orm(bike_model_test)
	assert bike_model_test_schema
	return bike_model_test_schema

@pytest.fixture
def bike_with_model_1(test_db: Session, bike_model_1: schemas.BikeModel):
	bike_test_model = Bike(
		model_id=bike_model_1.id,
		color='test_color_1',
		images=['image1', 'image2'],
		rate=1,
		rate_unit='hour',
	)
	bike_with_model_test = crud.bike.create_db_model(test_db, db_model_in=bike_test_model)
	assert bike_with_model_test
	bike_with_model_test_schema = schemas.BikeWithModel.from_orm(bike_with_model_test)
	assert bike_with_model_test_schema
	return bike_with_model_test_schema

@pytest.fixture
def bikes_with_model_2(test_db: Session, bike_model_2: schemas.BikeModel):
	bike_test_model = Bike(
		model_id=bike_model_2.id,
		color='test_color_2',
		images=['image3'],
		rate=2,
		rate_unit='hour',
	)
	bike_with_model_test = crud.bike.create_db_model(test_db, db_model_in=bike_test_model)
	assert bike_with_model_test
	bike_with_model_test_schema_1 = schemas.BikeWithModel.from_orm(bike_with_model_test)
	assert bike_with_model_test_schema_1

	bike_test_model = Bike(
		model_id=bike_model_2.id,
		color='test_color_3',
		images=['image4'],
		rate=3,
		rate_unit='hour',
	)
	bike_with_model_test = crud.bike.create_db_model(test_db, db_model_in=bike_test_model)
	assert bike_with_model_test
	bike_with_model_test_schema_2 = schemas.BikeWithModel.from_orm(bike_with_model_test)
	assert bike_with_model_test_schema_2

	return [bike_with_model_test_schema_1, bike_with_model_test_schema_2]

@pytest.fixture
def bikes_with_model(test_db: Session, bike_with_model_1: schemas.BikeWithModel,
					 bikes_with_model_2: List[schemas.BikeWithModel]):
	return [bike_with_model_1] + bikes_with_model_2