from typing import List, Optional
from .base import BaseRepository
from ..models import user as user_model

class UserRepository(BaseRepository[user_model.User, user_model.UserCreate]):
    def __init__(self):
        self._users = {}
        self._id_counter = 0

    def get(self, obj_id: int) -> Optional[user_model.User]:
        return self._users.get(obj_id)

    def list(self) -> List[user_model.User]:
        return list(self._users.values())

    def create(self, obj_in: user_model.UserCreate) -> user_model.User:
        self._id_counter += 1
        new_user = user_model.User(
            id=self._id_counter,
            email=obj_in.email,
            username=obj_in.username
        )
        self._users[new_user.id] = new_user
        return new_user

# Create a single instance to act as our "database"
user_repository = UserRepository()
