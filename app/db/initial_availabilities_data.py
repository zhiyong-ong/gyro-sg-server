from datetime import datetime

import pytz
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
import logging

logger = logging.getLogger(__name__)
# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.models import Transmission  # noqa

timezone = pytz.timezone('Asia/Singapore')

models = [
    {
        "start_datetime": datetime(2021, 9, 1, 10).astimezone(timezone),
        "end_datetime": datetime(2021, 9, 2, 15).astimezone(timezone),
        "bike_id": 1
    },
    {
        "start_datetime": datetime(2021, 9, 5, 10).astimezone(timezone),
        "end_datetime": datetime(2021, 9, 5, 15).astimezone(timezone),
        "bike_id": 1
    },
    {
        "start_datetime": datetime(2021, 9, 2, 10).astimezone(timezone),
        "end_datetime": datetime(2021, 9, 3, 16).astimezone(timezone),
        "bike_id": 2
    },
    {
        "start_datetime": datetime(2021, 11, 1, 10).astimezone(timezone),
        "end_datetime": datetime(2021, 11, 25, 16).astimezone(timezone),
        "bike_id": 4
    },
    {
        "start_datetime": datetime(2021, 11, 2, 8).astimezone(timezone),
        "end_datetime": datetime(2021, 11, 15, 17).astimezone(timezone),
        "bike_id": 3
    },
    {
        "start_datetime": datetime(2021, 11, 5, 6).astimezone(timezone),
        "end_datetime": datetime(2021, 11, 9, 17).astimezone(timezone),
        "bike_id": 6
    },
    {
        "start_datetime": datetime(2021, 11, 10, 10).astimezone(timezone),
        "end_datetime": datetime(2021, 11, 30, 16).astimezone(timezone),
        "bike_id": 5
    },
    {
        "start_datetime": datetime(2021, 11, 23, 10).astimezone(timezone),
        "end_datetime": datetime(2021, 11, 27, 16).astimezone(timezone),
        "bike_id": 3
    },
    {
        "start_datetime": datetime(2021, 11, 1, 10).astimezone(timezone),
        "end_datetime": datetime(2021, 11, 7, 16).astimezone(timezone),
        "bike_id": 7
    }
]


def initial_bike_availability_data(db: Session) -> None:
    logger.info("Creating initial availabilities data")
    count = 0
    for availability_data in models:
        if crud.transmission.get(db, id=availability_data.get("id")):
            continue
        bike_availability_model = schemas.BikeAvailabilityCreate(
            start_datetime=availability_data.get("start_datetime"),
            end_datetime=availability_data.get("end_datetime"),
            bike_id=availability_data.get("bike_id"),
        )
        crud.bike_availability.create(db, obj_in=bike_availability_model)
        count += 1
    logger.info(f"Created {count} initial availabilities data")
    db.execute(
        "SELECT setval('bike_availability_id_seq', (SELECT max(id) FROM bike_availability));"
    )
    db.commit()
