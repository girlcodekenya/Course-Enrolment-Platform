from pydantic import BaseModel, Field
from app.schemas.common import TimestampMixin
from typing import Optional


class CourseBase(BaseModel):
    title: str
    code: str
    capacity: int = Field(gt=0)


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None


class CourseResponse(CourseBase, TimestampMixin):
    is_active: bool
    enrolled_count: int = 0
    
    class Config:
        from_attributes = True