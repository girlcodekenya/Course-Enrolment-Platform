from pydantic import BaseModel
from app.schemas.common import TimestampMixin
from app.schemas.user import UserResponse
from app.schemas.course import CourseResponse
from typing import Optional


class EnrollmentBase(BaseModel):
    course_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentResponse(TimestampMixin):
    user_id: int
    course_id: int
    user: Optional[UserResponse] = None
    course: Optional[CourseResponse] = None
    
    class Config:
        from_attributes = True