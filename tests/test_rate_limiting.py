import pytest
from fastapi import status


def test_rate_limit_login(client, test_student):
    for i in range(6):
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "student@test.com", "password": "wrongpassword"}
        )
        if i < 5:
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
        else:
            assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS