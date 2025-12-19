from sqlalchemy.orm import Session
from ..models.pydantic import user as pydantic_user
from ..repositories.user_repository import UserRepository

def get_user(db: Session, user_id: int):
    """
    Retrieves a user by their ID using the repository.
    """
    repo = UserRepository()
    return repo.get_user(db=db, user_id=user_id)

def create_user(db: Session, user: pydantic_user.UserCreate):
    """
    Creates a new user using the repository.
    """
    repo = UserRepository()
    return repo.create_user(db=db, user=user)
