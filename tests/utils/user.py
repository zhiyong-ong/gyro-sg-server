
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import get_config, TEST
from app.schemas.user import UserCreate, UserUpdateInput

TEST_CONFIG = get_config(TEST)


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{TEST_CONFIG.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(
    *, client: TestClient, email: str, password: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(email=email, password=password, first_name="first", last_name="last")
        crud.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdateInput(password=password)
        crud.user.update_with_superuser(db, db_obj=user, obj_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)