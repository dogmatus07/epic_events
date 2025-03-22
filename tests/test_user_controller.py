import pytest
from crm.controllers import UserController
from crm.models.models import User

def test_create_user(db_session):
    """
    Test creating a user
    input: db_session
    output: User object
    """
    controller = UserController(db_session)
    user_data = {
        "username": "test_user",
        "email": "test_user@example.com",
        "phone_number": "1234567890",
        "is_active": True,
        "role_name": "Gestion",
        "hashed_password": "password123",
    }
    user = controller.create_user(user_data)
    assert isinstance(user, User)
    assert user.username == "test_user"