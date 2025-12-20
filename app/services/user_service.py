from sqlalchemy.orm import Session
from ..models.pydantic import user as pydantic_user
from ..repositories.user_repository import UserRepository
from app.models.orm.models import User as ORMUser
from ..core import security # Import security module
from typing import Optional

# Instantiate repository once
user_repository = UserRepository()

def authenticate_user(db: Session, username: str, password: str) -> Optional[ORMUser]:
    user = user_repository.get_user_by_username(db=db, username=username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user

def get_user(db: Session, user_id: int) -> Optional[ORMUser]:
    return user_repository.get_user(db=db, user_id=user_id)

def get_user_by_email(db: Session, email: str) -> Optional[ORMUser]:
    return user_repository.get_user_by_email(db=db, email=email)

def get_user_by_username(db: Session, username: str) -> Optional[ORMUser]:
    return user_repository.get_user_by_username(db=db, username=username)

def create_user(db: Session, user: pydantic_user.UserCreate) -> ORMUser:
    return user_repository.create_user(db=db, user=user)