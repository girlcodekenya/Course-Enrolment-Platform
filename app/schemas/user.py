from pydantic import BaseModel, EmailStr
from app.schemas.common import TimestampMixin


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: str = "student"


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class UserResponse(UserBase, TimestampMixin):
    role: str
    is_active: bool
    
    class Config:
        from_attributes = True