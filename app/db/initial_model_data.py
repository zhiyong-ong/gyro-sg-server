from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
import logging

logger = logging.getLogger(__name__)
# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.models import BikeModel  # noqa

models = [
    {"id": 1, "name": "Vespa LX150"},
    {"id": 2, "name": "KTM Duke 200"},
    {"id": 3, "name": "Vespa GTS300 Super"},
    {"id": 4, "name": "KTM Duke 390"},
    {"id": 5, "name": "Honda MSX125"},
    {"id": 6, "name": "Yamaha RXZ"},
]


def initial_model_data(db: Session) -> None:
    logger.info("Creating initial bike model data")
    count = 0
    for bike_model_data in models:
        if crud.bike_model.get(db, id=bike_model_data.get("id")):
            continue
        bike_model = schemas.BikeModel(
            id=bike_model_data.get("id"), name=bike_model_data.get("name")
        )
        crud.bike_model.create(db, obj_in=bike_model)
        count += 1
    logger.info(f"Created {count} initial bike model data")
    db.execute("SELECT setval('bike_model_id_seq', (SELECT max(id) FROM bike_model));")
    db.commit()
