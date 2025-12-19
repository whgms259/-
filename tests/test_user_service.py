import pytest
from app.services import user_service
from app.models import user as user_model

def test_create_user():
    """
    Test creating a user.
    """
    user_to_create = user_model.UserCreate(
        email="test@example.com",
        username="testuser",
        password="password"
    )
    
    new_user = user_service.create_user(user=user_to_create)
    
    assert new_user is not None
    assert new_user.email == user_to_create.email
    assert new_user.username == user_to_create.username
    assert hasattr(new_user, 'id')
    assert new_user.id is not None

    # Check if the user was "saved" in our fake db
    saved_user = user_service.get_user(new_user.id)
    assert saved_user == new_user
