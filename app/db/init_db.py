from sqlalchemy.orm import Session

from app import crud
from app.core.config import CONFIG
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.models import User


def init_db(db: Session) -> None:
    user = crud.user.get_by_email(db, email=CONFIG.FIRST_SUPERUSER)
    if not user:
        user_in = User(
            email=CONFIG.FIRST_SUPERUSER,
            password_hash=CONFIG.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud.user.create_db_model(db, db_model_in=user_in)
