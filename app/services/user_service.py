from sqlalchemy.orm import Session
from ..models.pydantic import user as pydantic_user
from ..repositories.user_repository import UserRepository
from typing import Optional

# Instantiate repository once
user_repository = UserRepository()

def get_user(db: Session, user_id: int) -> Optional[pydantic_user.User]:
    return user_repository.get_user(db=db, user_id=user_id)

def get_user_by_email(db: Session, email: str) -> Optional[pydantic_user.User]:
    return user_repository.get_user_by_email(db=db, email=email)

def get_user_by_username(db: Session, username: str) -> Optional[pydantic_user.User]:
    return user_repository.get_user_by_username(db=db, username=username)

def create_user(db: Session, user: pydantic_user.UserCreate) -> pydantic_user.User:
    return user_repository.create_user(db=db, user=user)