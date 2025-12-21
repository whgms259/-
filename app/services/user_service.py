from sqlalchemy.orm import Session
from ..models.pydantic import user as pydantic_user
from ..repositories.user_repository import UserRepository
from app.models.orm.models import User as ORMUser
from ..core import security
from typing import Optional

# Instantiate repository once
user_repository = UserRepository()

def authenticate_user(db: Session, username: str, password: str) -> Optional[ORMUser]:
    print(f"DEBUG: Authenticating user '{username}'")
    hashed_username = security.get_field_hash(username)
    print(f"DEBUG: Hashed username for lookup: '{hashed_username}'")
    user = user_repository.get_user_by_username(db=db, username=hashed_username)
    if not user:
        print(f"DEBUG: User '{username}' not found with hashed username '{hashed_username}'")
        return None
    print(f"DEBUG: User '{username}' found, verifying password...")
    if not security.verify_password(password, user.hashed_password):
        print(f"DEBUG: Password verification failed for user '{username}'")
        return None
    print(f"DEBUG: User '{username}' authenticated successfully.")
    return user

def get_user(db: Session, user_id: int) -> Optional[ORMUser]:
    return user_repository.get_user(db=db, user_id=user_id)

def get_user_by_email(db: Session, email: str) -> Optional[ORMUser]:
    hashed_email = security.get_field_hash(email)
    return user_repository.get_user_by_email(db=db, email=hashed_email)

def get_user_by_username(db: Session, username: str) -> Optional[ORMUser]:
    hashed_username = security.get_field_hash(username)
    return user_repository.get_user_by_username(db=db, username=hashed_username)

def create_user(db: Session, user: pydantic_user.UserCreate) -> ORMUser:
    user_data = user.model_dump()
    user_data["hashed_password"] = security.get_password_hash(user.password)
    del user_data["password"]

    user_data["email"] = security.get_field_hash(user.email)
    user_data["username"] = security.get_field_hash(user.username)
    
    return user_repository.create_user(db=db, user_data=user_data)