from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
import logging

logger = logging.getLogger(__name__)
# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.models import LicenceClass  # noqa

models = [
    {"id": 1, "name": "Class 2", "description": "400cc and above"},
    {"id": 2, "name": "Class 2A", "description": "201cc - 400cc"},
    {"id": 3, "name": "Class 2B", "description": "200cc and below"},
]


def initial_licence_class_data(db: Session) -> None:
    logger.info("Creating initial licence class data")
    count = 0
    for licence_class_data in models:
        if crud.licence_class.get(db, id=licence_class_data.get("id")):
            continue
        licence_class_model = schemas.LicenceClassCreateWithId(
            id=licence_class_data.get("id"),
            name=licence_class_data.get("name"),
            description=licence_class_data.get("description"),
        )
        crud.licence_class.create(db, obj_in=licence_class_model)
        count += 1
    logger.info(f"Created {count} initial licence class data")
    db.execute(
        "SELECT setval('licence_class_id_seq', (SELECT max(id) FROM licence_class));"
    )
    db.commit()
