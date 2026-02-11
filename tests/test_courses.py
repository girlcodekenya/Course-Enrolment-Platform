import pytest
from fastapi import status


def test_list_courses_public(client, db):
    response = client.get("/api/v1/courses")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_course_as_admin(client, admin_token):
    response = client.post(
        "/api/v1/courses",
        json={
            "title": "Introduction to Python",
            "code": "CS101",
            "capacity": 30
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Introduction to Python"
    assert data["code"] == "CS101"
    assert data["capacity"] == 30


def test_create_course_as_student_fails(client, student_token):
    response = client.post(
        "/api/v1/courses",
        json={
            "title": "Unauthorized Course",
            "code": "CS999",
            "capacity": 20
        },
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_course_duplicate_code(client, admin_token):
    client.post(
        "/api/v1/courses",
        json={"title": "Course 1", "code": "CS101", "capacity": 30},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    response = client.post(
        "/api/v1/courses",
        json={"title": "Course 2", "code": "CS101", "capacity": 20},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_course_invalid_capacity(client, admin_token):
    response = client.post(
        "/api/v1/courses",
        json={"title": "Invalid Course", "code": "CS000", "capacity": 0},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_course_as_admin(client, admin_token):
    create_response = client.post(
        "/api/v1/courses",
        json={"title": "Original Title", "code": "CS101", "capacity": 30},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    course_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/v1/courses/{course_id}",
        json={"title": "Updated Title"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Updated Title"


def test_delete_course_as_admin(client, admin_token):
    create_response = client.post(
        "/api/v1/courses",
        json={"title": "To Delete", "code": "CS999", "capacity": 10},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    course_id = create_response.json()["id"]
    
    response = client.delete(
        f"/api/v1/courses/{course_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT