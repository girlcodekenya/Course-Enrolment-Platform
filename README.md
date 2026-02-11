# Course Enrollment Platform

A secure, database-backed RESTful API built with FastAPI for managing course enrollments with role-based access control.

## Features

- JWT Authentication & Authorization
- Role-Based Access Control (Student/Admin)
- Course Management
- Enrollment System with Business Rules
- Soft Deletes
- Audit Logging
- Rate Limiting
- Pagination & Filtering
- Comprehensive Test Suite

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (Migrations)
- Pytest
- JWT Authentication

## Setup Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

1. Clone the repository
2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
copy .env.example .env
```

5. Update `.env` with your database credentials

6. Run migrations:
```bash
alembic upgrade head
```

7. Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation at `http://localhost:8000/docs`

## Running Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

Run specific test file:
```bash
pytest tests/test_auth.py
```

## Project Structure

```
course_enrollment_platform/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── courses.py
│   │   │   └── enrollments.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── rate_limiter.py
│   ├── models/
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── enrollment.py
│   │   └── audit_log.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── enrollment.py
│   │   └── auth.py
│   ├── services/
│   │   ├── user_service.py
│   │   ├── course_service.py
│   │   └── enrollment_service.py
│   ├── utils/
│   │   └── pagination.py
│   ├── database.py
│   └── main.py
├── alembic/
├── tests/
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Users
- `GET /api/v1/users/me` - Get current user profile

### Courses
- `GET /api/v1/courses` - List all courses (public)
- `GET /api/v1/courses/{id}` - Get course details (public)
- `POST /api/v1/courses` - Create course (admin only)
- `PUT /api/v1/courses/{id}` - Update course (admin only)
- `DELETE /api/v1/courses/{id}` - Delete course (admin only)

### Enrollments
- `POST /api/v1/enrollments` - Enroll in course (student)
- `DELETE /api/v1/enrollments/{id}` - Deregister from course (student)
- `GET /api/v1/enrollments` - Get all enrollments (admin)
- `GET /api/v1/enrollments/course/{course_id}` - Get course enrollments (admin)

## Business Rules

### Enrollment Rules
- Students can only enroll in active courses
- Cannot enroll in the same course twice
- Enrollment fails if course is at capacity
- Only authenticated students can enroll

### Course Rules
- Course code must be unique
- Capacity must be greater than zero
- Only admins can create/update/delete courses

### User Rules
- Email must be unique
- Inactive users cannot authenticate
- Passwords are securely hashed

## Deployment

Deployed on Railway: [Add your deployment URL]

## License

MIT