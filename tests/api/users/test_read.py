from typing import List, Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import schemas


def test_read_users(
    client: TestClient,
    user: schemas.UserWithId,
    superuser_headers: Dict[str, str],
):
    response = client.get("/api/v1/users", headers=superuser_headers)
    assert response.status_code == 200
    user_list = response.json()
    assert len(user_list) == 2
    assert "password" not in user_list[0]


def test_read_users_basic_user(
    client: TestClient,
    user: schemas.UserWithId,
    user_headers: Dict[str, str],
):
    response = client.get("/api/v1/users", headers=user_headers)
    assert response.status_code == 400


def test_read_user(
    client: TestClient,
    user: schemas.UserWithId,
    superuser_headers: Dict[str, str],
):
    response = client.get(f"/api/v1/users/{user.id}", headers=superuser_headers)
    assert response.status_code == 200
    user_details = response.json()
    assert user_details["email"] == user.email
    assert "password" not in user_details


def test_read_user_basic_user(
    client: TestClient,
    user: schemas.UserWithId,
    user_headers: Dict[str, str],
):
    response = client.get(f"/api/v1/users/{user.id}", headers=user_headers)
    assert response.status_code == 400


def test_read_user_missing_user(
    client: TestClient,
    user: schemas.UserWithId,
    superuser_headers: Dict[str, str],
):
    response = client.get(f"/api/v1/users/99", headers=superuser_headers)
    assert response.status_code == 404


def test_read_current_user_basic_user(
    client: TestClient,
    user: schemas.UserWithId,
    user_headers: Dict[str, str],
):
    response = client.get("/api/v1/users/me", headers=user_headers)
    assert response.status_code == 200
    user_details = response.json()
    assert user_details
    assert user_details["email"] == user.email
    assert user_details["first_name"] == user.first_name
    assert user_details["last_name"] == user.last_name
    assert user_details["is_superuser"] == user.is_superuser
    assert user_details["is_active"] == user.is_active
    assert "password" not in user_details
