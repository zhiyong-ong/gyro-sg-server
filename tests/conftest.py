from contextlib import contextmanager
from functools import partial
from typing import Iterator, Dict

import pytest
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient

from app import schemas, crud
from app.api.deps import get_db
from app.db.base_class import Base
from app.core.config import get_config, TEST
from app.main import app

TEST_CONFIG = get_config(TEST)

engine = create_engine(TEST_CONFIG.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def database_context_manager():
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


@pytest.fixture
def get_test_db():
    with database_context_manager() as db:
        yield db


@pytest.fixture
def test_db(get_test_db: Session):
    get_test_db.commit()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return get_test_db


def override_get_db(test_db: Session) -> Iterator[Session]:
    try:
        yield test_db
    finally:
        test_db.close()


@pytest.fixture
def client(test_db: Session) -> TestClient:
    app.dependency_overrides[get_db] = partial(override_get_db, test_db)
    return TestClient(app)

@pytest.fixture
def superuser(client: TestClient, test_db: Session) -> schemas.UserWithId:
    user_in = schemas.UserCreateSuperuser(
        email=TEST_CONFIG.FIRST_SUPERUSER,
        password=TEST_CONFIG.FIRST_SUPERUSER_PASSWORD,
        first_name="gyrosg",
        last_name="admin",
        is_superuser=True,
    )
    user_model = crud.user.create_superuser(test_db, obj_in=user_in)
    return schemas.UserWithId.from_orm(user_model)


@pytest.fixture
def superuser_headers(client: TestClient, superuser: schemas.UserWithId) -> Dict[str, str]:
    login_data = {
        "username": TEST_CONFIG.FIRST_SUPERUSER,
        "password": TEST_CONFIG.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post(
        f"{TEST_CONFIG.API_V1_STR}/login/access-token", data=login_data
    )
    token_response = response.json()
    assert token_response
    auth_token = token_response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
