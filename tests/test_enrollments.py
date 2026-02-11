import pytest
from fastapi import status


@pytest.fixture
def test_course(client, admin_token):
    response = client.post(
        "/api/v1/courses",
        json={"title": "Test Course", "code": "TEST101", "capacity": 2},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    return response.json()


def test_enroll_in_course(client, student_token, test_course):
    response = client.post(
        "/api/v1/enrollments",
        json={"course_id": test_course["id"]},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["course_id"] == test_course["id"]


def test_enroll_twice_fails(client, student_token, test_course):
    client.post(
        "/api/v1/enrollments",
        json={"course_id": test_course["id"]},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    
    response = client.post(
        "/api/v1/enrollments",
        json={"course_id": test_course["id"]},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Already enrolled" in response.json()["detail"]


def test_enroll_in_full_course_fails(client, admin_token, db):
    course_response = client.post(
        "/api/v1/courses",
        json={"title": "Full Course", "code": "FULL101", "capacity": 1},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    course_id = course_response.json()["id"]
    
    student1_response = client.post(
        "/api/v1/auth/register",
        json={"name": "Student 1", "email": "s1@test.com", "password": "pass", "role": "student"}
    )
    student1_login = client.post(
        "/api/v1/auth/login",
        data={"username": "s1@test.com", "password": "pass"}
    )
    token1 = student1_login.json()["access_token"]
    
    client.post(
        "/api/v1/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    student2_response = client.post(
        "/api/v1/auth/register",
        json={"name": "Student 2", "email": "s2@test.com", "password": "pass", "role": "student"}
    )
    student2_login = client.post(
        "/api/v1/auth/login",
        data={"username": "s2@test.com", "password": "pass"}
    )
    token2 = student2_login.json()["access_token"]
    
    response = client.post(
        "/api/v1/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "full capacity" in response.json()["detail"]


def test_unenroll_from_course(client, student_token, test_course):
    enroll_response = client.post(
        "/api/v1/enrollments",
        json={"course_id": test_course["id"]},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    enrollment_id = enroll_response.json()["id"]
    
    response = client.delete(
        f"/api/v1/enrollments/{enrollment_id}",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_list_all_enrollments_as_admin(client, admin_token, student_token, test_course):
    client.post(
        "/api/v1/enrollments",
        json={"course_id": test_course["id"]},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    
    response = client.get(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_list_enrollments_as_student_fails(client, student_token):
    response = client.get(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN