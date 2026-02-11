from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from app.services.enrollment_service import EnrollmentService
from app.services.course_service import CourseService
from app.services.audit_service import AuditService
from app.models.user import User
from app.api.deps import get_current_student, get_current_admin, get_current_user

router = APIRouter()


@router.post("", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_in_course(
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    course = CourseService.get_by_id(db, enrollment_data.course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    enrollment = EnrollmentService.enroll(db, current_user, course)
    
    AuditService.log_action(
        db=db,
        action="STUDENT_ENROLLED",
        entity_type="enrollment",
        entity_id=enrollment.id,
        user_id=current_user.id,
        details={"course_id": course.id, "course_code": course.code}
    )
    
    return enrollment


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def unenroll_from_course(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    enrollment = EnrollmentService.get_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    if enrollment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot unenroll from another student's enrollment"
        )
    
    EnrollmentService.unenroll(db, enrollment)
    
    AuditService.log_action(
        db=db,
        action="STUDENT_UNENROLLED",
        entity_type="enrollment",
        entity_id=enrollment.id,
        user_id=current_user.id
    )
    
    return None


@router.get("", response_model=List[EnrollmentResponse])
def list_all_enrollments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    enrollments = EnrollmentService.get_all(db, skip=skip, limit=limit)
    return enrollments


@router.get("/course/{course_id}", response_model=List[EnrollmentResponse])
def list_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    course = CourseService.get_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    enrollments = EnrollmentService.get_by_course(db, course_id)
    return enrollments


@router.get("/my-enrollments", response_model=List[EnrollmentResponse])
def list_my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enrollments = EnrollmentService.get_by_user(db, current_user.id)
    return enrollments