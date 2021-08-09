from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import CONFIG
from app.db import base  # noqa: F401
import logging

logger = logging.getLogger(__name__)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.models import User  # noqa


def initial_user_data(db: Session) -> None:
    user = crud.user.get_by_email(db, email=CONFIG.FIRST_SUPERUSER)
    count = 0
    logger.info("Creating initial user data")
    if not user:
        user_in = schemas.UserCreateSuperuser(
            email=CONFIG.FIRST_SUPERUSER,
            password=CONFIG.FIRST_SUPERUSER_PASSWORD,
            first_name="gyrosg",
            last_name="admin",
            is_superuser=True,
        )
        crud.user.create_superuser(db, obj_in=user_in)
        count += 1
    logger.info(f"Created {count} initial user data")
