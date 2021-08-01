from contextlib import contextmanager
from functools import partial
from typing import Iterator

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
	init_db(db)
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
		return db


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
def client(get_test_db: Session) -> TestClient:
	app.dependency_overrides[get_db] = partial(override_get_db, get_test_db)
	return TestClient(app)
