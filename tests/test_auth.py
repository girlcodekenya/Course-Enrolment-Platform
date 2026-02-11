import pytest
from fastapi import status


def test_register_student(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "New Student",
            "email": "newstudent@test.com",
            "password": "password123",
            "role": "student"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "newstudent@test.com"
    assert data["role"] == "student"
    assert "hashed_password" not in data


def test_register_admin(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "New Admin",
            "email": "newadmin@test.com",
            "password": "password123",
            "role": "admin"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["role"] == "admin"


def test_register_duplicate_email(client, test_student):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Duplicate",
            "email": "student@test.com",
            "password": "password123",
            "role": "student"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in response.json()["detail"]


def test_register_invalid_role(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Invalid Role",
            "email": "invalid@test.com",
            "password": "password123",
            "role": "teacher"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(client, test_student):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "student@test.com", "password": "password123"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_student):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "student@test.com", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_nonexistent_user(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistent@test.com", "password": "password123"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED