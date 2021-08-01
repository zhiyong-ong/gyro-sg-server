from typing import Dict

import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from tests.utils.user import authentication_token_from_email


@pytest.fixture
def user_headers(client: TestClient, test_db: Session) -> Dict[str, str]:
	test_user = "test_user@example.com"
	test_password = "password"
	headers = authentication_token_from_email(client=client, email=test_user, password=test_password, db=test_db)
	return headers