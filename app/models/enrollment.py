from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Enrollment(BaseModel):
    __tablename__ = "enrollments"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")