import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    return TestClient(app)


@pytest.fixture(scope="function")
def test_student(db):
    user = User(
        name="Test Student",
        email="student@test.com",
        hashed_password=get_password_hash("password123"),
        role=UserRole.STUDENT,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_admin(db):
    user = User(
        name="Test Admin",
        email="admin@test.com",
        hashed_password=get_password_hash("password123"),
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def student_token(client, test_student):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "student@test.com", "password": "password123"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def admin_token(client, test_admin):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@test.com", "password": "password123"}
    )
    return response.json()["access_token"]