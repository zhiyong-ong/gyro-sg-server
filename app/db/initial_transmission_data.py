from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
import logging

logger = logging.getLogger(__name__)
# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.models import Transmission  # noqa

models = [
    {"id": 1, "name": "Automatic", "description": "No clutch, no gears"},
    {"id": 2, "name": "Manual", "description": "Has clutch, has gears"},
    {"id": 3, "name": "Semi-automatic", "description": "No clutch, has gears"},
]


def initial_transmission_data(db: Session) -> None:
    logger.info("Creating initial transmission data")
    count = 0
    for transmission_data in models:
        if crud.transmission.get(db, id=transmission_data.get("id")):
            continue
        bike_model = schemas.Transmission(
            id=transmission_data.get("id"),
            name=transmission_data.get("name"),
            description=transmission_data.get("description"),
        )
        crud.transmission.create(db, obj_in=bike_model)
        count += 1
    logger.info(f"Created {count} initial transmission data")
    db.execute(
        "SELECT setval('transmission_id_seq', (SELECT max(id) FROM transmission));"
    )
    db.commit()
