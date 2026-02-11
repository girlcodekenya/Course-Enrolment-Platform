from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from typing import Optional


class UserService:
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(
            User.id == user_id,
            User.is_deleted == False
        ).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(
            User.email == email,
            User.is_deleted == False
        ).first()
    
    @staticmethod
    def create(db: Session, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        
        user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            role=UserRole(user_data.role)
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update(db: Session, user: User, user_data: UserUpdate) -> User:
        update_data = user_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user