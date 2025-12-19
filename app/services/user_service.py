from ..models import user as user_model
from ..repositories.user_repository import user_repository

def get_user(user_id: int):
    """
    Retrieves a user by their ID using the repository.
    """
    return user_repository.get(obj_id=user_id)

def create_user(user: user_model.UserCreate):
    """
    Creates a new user using the repository.
    """
    return user_repository.create(obj_in=user)
