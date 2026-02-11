from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment
from app.models.user import User
from app.models.course import Course
from app.schemas.enrollment import EnrollmentCreate
from typing import Optional, List
from datetime import datetime
from fastapi import HTTPException, status


class EnrollmentService:
    
    @staticmethod
    def get_by_id(db: Session, enrollment_id: int) -> Optional[Enrollment]:
        return db.query(Enrollment).filter(
            Enrollment.id == enrollment_id,
            Enrollment.is_deleted == False
        ).first()
    
    @staticmethod
    def get_user_enrollment(db: Session, user_id: int, course_id: int) -> Optional[Enrollment]:
        return db.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id,
            Enrollment.is_deleted == False
        ).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Enrollment]:
        return db.query(Enrollment).filter(
            Enrollment.is_deleted == False
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_course(db: Session, course_id: int) -> List[Enrollment]:
        return db.query(Enrollment).filter(
            Enrollment.course_id == course_id,
            Enrollment.is_deleted == False
        ).all()
    
    @staticmethod
    def get_by_user(db: Session, user_id: int) -> List[Enrollment]:
        return db.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.is_deleted == False
        ).all()
    
    @staticmethod
    def enroll(db: Session, user: User, course: Course) -> Enrollment:
        if not course.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot enroll in an inactive course"
            )
        
        existing_enrollment = EnrollmentService.get_user_enrollment(db, user.id, course.id)
        if existing_enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already enrolled in this course"
            )
        
        if course.is_full:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course is at full capacity"
            )
        
        enrollment = Enrollment(user_id=user.id, course_id=course.id)
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return enrollment
    
    @staticmethod
    def unenroll(db: Session, enrollment: Enrollment) -> Enrollment:
        enrollment.is_deleted = True
        enrollment.deleted_at = datetime.utcnow()
        db.commit()
        db.refresh(enrollment)
        return enrollment