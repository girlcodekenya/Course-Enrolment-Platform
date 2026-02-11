from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from typing import Optional, List
from datetime import datetime


class CourseService:
    
    @staticmethod
    def get_by_id(db: Session, course_id: int, include_deleted: bool = False) -> Optional[Course]:
        query = db.query(Course).filter(Course.id == course_id)
        if not include_deleted:
            query = query.filter(Course.is_deleted == False)
        return query.first()
    
    @staticmethod
    def get_by_code(db: Session, code: str) -> Optional[Course]:
        return db.query(Course).filter(
            Course.code == code,
            Course.is_deleted == False
        ).first()
    
    @staticmethod
    def get_all(db: Session, active_only: bool = False, skip: int = 0, limit: int = 100) -> List[Course]:
        query = db.query(Course).filter(Course.is_deleted == False)
        
        if active_only:
            query = query.filter(Course.is_active == True)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, course_data: CourseCreate) -> Course:
        course = Course(**course_data.model_dump())
        db.add(course)
        db.commit()
        db.refresh(course)
        return course
    
    @staticmethod
    def update(db: Session, course: Course, course_data: CourseUpdate) -> Course:
        update_data = course_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(course, field, value)
        
        db.commit()
        db.refresh(course)
        return course
    
    @staticmethod
    def soft_delete(db: Session, course: Course) -> Course:
        course.is_deleted = True
        course.deleted_at = datetime.utcnow()
        db.commit()
        db.refresh(course)
        return course