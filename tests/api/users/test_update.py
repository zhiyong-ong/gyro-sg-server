from typing import Dict, Tuple

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import schemas, crud
from tests.api.conftest import password
from tests.utils.user import user_authentication_headers


def test_update_current_user(
    client: TestClient,
    test_db: Session,
    user: schemas.UserWithId,
    user_headers: Dict[str, str],
):
    update_data = {
        "mobile_number": "12345",
    }
    response = client.patch(
        f"/api/v1/users/me",
        headers=user_headers,
        json=update_data,
    )
    assert response.status_code == 200
    user_details = response.json()
    assert user_details
    assert user_details["mobile_number"] == "12345"
    assert "password" not in user_details

    ret_user = crud.user.get(test_db, id=user.id)
    assert ret_user
    assert ret_user.mobile_number == "12345"


def test_update_current_user_superuser_invalid(
    client: TestClient,
    user_headers: Dict[str, str],
):
    update_data = {
        "is_superuser": True,
    }
    response = client.patch(
        f"/api/v1/users/me",
        headers=user_headers,
        json=update_data,
    )
    assert response.status_code == 422


def test_update_current_user_password(
    client: TestClient,
    user: schemas.UserWithId,
    user_headers: Dict[str, str],
):
    update_data = {
        "cur_password": password,
        "new_password": "new password",
    }
    response = client.patch(
        f"/api/v1/users/me/password",
        headers=user_headers,
        json=update_data,
    )
    assert response.status_code == 200
    user_details = response.json()
    assert user_details
    assert "password" not in user_details

    assert user_authentication_headers(
        client=client, email=user.email, password="new password"
    )


def test_update_current_user_password_incorrect_password(
    client: TestClient,
    user: schemas.UserWithId,
    user_headers: Dict[str, str],
):
    update_data = {
        "cur_password": password + "abc",
        "new_password": "new password",
    }
    response = client.patch(
        f"/api/v1/users/me/password",
        headers=user_headers,
        json=update_data,
    )
    assert response.status_code == 400


def test_update_user(
    client: TestClient,
    user: schemas.UserWithId,
    test_db: Session,
    superuser_headers: Dict[str, str],
):
    update_data = {
        "is_superuser": True,
    }
    response = client.patch(
        f"/api/v1/users/{user.id}",
        headers=superuser_headers,
        json=update_data,
    )
    assert response.status_code == 200
    user_details = response.json()
    assert user_details
    assert user_details["is_superuser"] is True
    assert "password" not in user_details

    ret_user = crud.user.get(test_db, id=user.id)
    assert ret_user
    assert ret_user.is_superuser is True


def test_update_user_basic_user(
    client: TestClient,
    user: schemas.UserWithId,
    user_headers: Dict[str, str],
):
    update_data = {
        "is_superuser": True,
    }
    response = client.patch(
        f"/api/v1/users/{user.id}",
        headers=user_headers,
        json=update_data,
    )
    assert response.status_code == 400


def test_update_user_missing_user(
    client: TestClient,
    user: schemas.UserWithId,
    superuser_headers: Dict[str, str],
):
    update_data = {
        "is_superuser": True,
    }
    response = client.patch(
        f"/api/v1/users/99",
        headers=superuser_headers,
        json=update_data,
    )
    assert response.status_code == 404
