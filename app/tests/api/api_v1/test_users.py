from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import user as crud_user
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/user/me",
                   headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_get_existing_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud_user.user.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/user/{user_id}", headers=normal_user_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud_user.user.get_by_email(db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_retrieve_users(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud_user.user.create(db, obj_in=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    crud_user.user.create(db, obj_in=user_in2)

    r = client.get(f"{settings.API_V1_STR}/user/",
                   headers=normal_user_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item


def test_register_user(
    client: TestClient, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    full_name = random_lower_string()

    register_data = {
        "password": password,
        "email": username,
        "full_name": full_name,
    }

    r = client.post(f"{settings.API_V1_STR}/user/register", json=register_data)

    user_data = r.json()

    user = crud_user.user.get(db, id=user_data.get("id"))

    assert 200 <= r.status_code < 300
    assert user
    assert user_data.get("id") == user.id
    assert user_data.get("full_name") == user.full_name
    assert user_data.get('email') == user.email
    assert user.is_active == True


def test_already_exist_user_register(
    client: TestClient, db: Session
):
    username = random_email()
    password = random_lower_string()
    full_name = random_lower_string()

    user_in = UserCreate(email=username, password=password)
    crud_user.user.create(db, obj_in=user_in)

    register_data = {
        "password": password,
        "email": username,
        "full_name": full_name,
    }

    r = client.post(f"{settings.API_V1_STR}/user/register", json=register_data)

    assert r.status_code == 400
