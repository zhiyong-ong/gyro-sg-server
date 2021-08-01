import random
import string
from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import get_config, TEST

TEST_CONFIG = get_config(TEST)


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": TEST_CONFIG.FIRST_SUPERUSER,
        "password": TEST_CONFIG.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{TEST_CONFIG.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers