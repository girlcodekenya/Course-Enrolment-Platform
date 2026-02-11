from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Course(BaseModel):
    __tablename__ = "courses"
    
    title = Column(String, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    
    @property
    def enrolled_count(self):
        return len([e for e in self.enrollments if not e.is_deleted])
    
    @property
    def is_full(self):
        return self.enrolled_count >= self.capacity