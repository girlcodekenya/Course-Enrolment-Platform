import pytest
from fastapi import status


def test_get_current_user_profile(client, student_token):
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "student@test.com"
    assert data["role"] == "student"


def test_get_profile_without_token(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_profile_with_invalid_token(client):
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED