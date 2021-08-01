from contextlib import contextmanager
from functools import partial
from typing import Iterator, Dict

import pytest
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient

from app.api.deps import get_db
from app.db.base_class import Base
from app.core.config import get_config, TEST
from app.db.init_db import init_db
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
    init_db(get_test_db)
    return get_test_db


def override_get_db(get_test_db: Session) -> Iterator[Session]:
    try:
        yield get_test_db
    finally:
        get_test_db.close()


@pytest.fixture
def client(get_test_db: Session) -> TestClient:
    app.dependency_overrides[get_db] = partial(override_get_db, get_test_db)
    return TestClient(app)


@pytest.fixture
def superuser_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": TEST_CONFIG.FIRST_SUPERUSER,
        "password": TEST_CONFIG.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post(
        f"{TEST_CONFIG.API_V1_STR}/login/access-token", data=login_data
    )
    tokens = response.json()
    auth_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
