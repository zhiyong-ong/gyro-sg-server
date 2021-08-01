from typing import Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import schemas


def test_create_user_open(
    client: TestClient,
    test_db: Session,
):
    data = {
        "email": "test123@example.com",
        "password": "password",
        "first_name": "first",
        "last_name": "last",
    }
    response = client.post("/api/v1/users/open", json=data)
    assert response.status_code == 201
    user_details = response.json()
    assert user_details["email"] == "test123@example.com"
    assert user_details["first_name"] == "first"
    assert user_details["last_name"] == "last"
    assert "password" not in user_details


def test_create_user_open_superuser_invalid(
    client: TestClient,
):
    data = {
        "email": "test123@example.com",
        "password": "password",
        "first_name": "first",
        "last_name": "last",
        "is_superuser": True,
    }
    response = client.post("/api/v1/users/open", json=data)
    assert response.status_code == 422


def test_create_user_open_conflict(
    client: TestClient,
    user: schemas.UserWithId,
):
    data = {
        "email": user.email,
        "password": "password",
        "first_name": "first",
        "last_name": "last",
    }
    response = client.post("/api/v1/users/open", json=data)
    assert response.status_code == 409


def test_create_user_superuser(client: TestClient, superuser_headers: Dict[str, str]):
    data = {
        "email": "test123@example.com",
        "password": "password",
        "first_name": "first",
        "last_name": "last",
        "is_superuser": True,
    }
    response = client.post("/api/v1/users", headers=superuser_headers, json=data)
    assert response.status_code == 201
    user_details = response.json()
    assert user_details["email"] == "test123@example.com"
    assert user_details["first_name"] == "first"
    assert user_details["last_name"] == "last"
    assert user_details["is_superuser"] is True
    assert "password" not in user_details


def test_create_user_superuser_basic_user(
    client: TestClient, user_headers: Dict[str, str]
):
    data = {
        "email": "test123@example.com",
        "password": "password",
        "first_name": "first",
        "last_name": "last",
        "is_superuser": True,
    }
    response = client.post("/api/v1/users", headers=user_headers, json=data)
    assert response.status_code == 400
