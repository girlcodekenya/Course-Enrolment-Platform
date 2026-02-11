from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.schemas.common import PaginationParams, PaginatedResponse
from app.services.course_service import CourseService
from app.services.audit_service import AuditService
from app.models.user import User
from app.api.deps import get_current_admin
from app.utils.pagination import paginate

router = APIRouter()


@router.get("", response_model=List[CourseResponse])
def list_courses(
    active_only: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    courses = CourseService.get_all(db, active_only=active_only, skip=skip, limit=limit)
    
    response_courses = []
    for course in courses:
        course_dict = CourseResponse.model_validate(course).model_dump()
        course_dict['enrolled_count'] = course.enrolled_count
        response_courses.append(CourseResponse(**course_dict))
    
    return response_courses


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = CourseService.get_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    course_dict = CourseResponse.model_validate(course).model_dump()
    course_dict['enrolled_count'] = course.enrolled_count
    
    return CourseResponse(**course_dict)


@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    existing_course = CourseService.get_by_code(db, course_data.code)
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course code already exists"
        )
    
    if course_data.capacity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Capacity must be greater than zero"
        )
    
    course = CourseService.create(db, course_data)
    
    AuditService.log_action(
        db=db,
        action="COURSE_CREATED",
        entity_type="course",
        entity_id=course.id,
        user_id=current_user.id,
        details={"code": course.code, "title": course.title}
    )
    
    course_dict = CourseResponse.model_validate(course).model_dump()
    course_dict['enrolled_count'] = course.enrolled_count
    
    return CourseResponse(**course_dict)


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    course = CourseService.get_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course_data.code:
        existing_course = CourseService.get_by_code(db, course_data.code)
        if existing_course and existing_course.id != course_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course code already exists"
            )
    
    if course_data.capacity is not None and course_data.capacity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Capacity must be greater than zero"
        )
    
    course = CourseService.update(db, course, course_data)
    
    AuditService.log_action(
        db=db,
        action="COURSE_UPDATED",
        entity_type="course",
        entity_id=course.id,
        user_id=current_user.id
    )
    
    course_dict = CourseResponse.model_validate(course).model_dump()
    course_dict['enrolled_count'] = course.enrolled_count
    
    return CourseResponse(**course_dict)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
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
    
    CourseService.soft_delete(db, course)
    
    AuditService.log_action(
        db=db,
        action="COURSE_DELETED",
        entity_type="course",
        entity_id=course.id,
        user_id=current_user.id
    )
    
    return None