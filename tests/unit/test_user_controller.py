import pytest
import uuid
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
        "id": str(uuid.uuid4()),
        "username": "test_user",
        "email": "test_user@example.com",
        "phone_number": "1234567890",
        "is_active": True,
        "role_name": "Gestion",
        "password": "password123",
    }
    user = controller.create_user(user_data)
    assert isinstance(user, User)
    assert user.username == "test_user"

def test_get_user(db_session):
    """
    Test getting a user
    input: db_session
    output: User object
    """
    controller = UserController(db_session)
    users = controller.get_all_users()
    assert isinstance(users, list)

def test_update_user(db_session):
    """
    Test updating a user
    input: db_session
    output: Updated User object
    """

    controller = UserController(db_session)
    user_data = {
        "id": str(uuid.uuid4()),
        "username": "test_user",
        "email": "test.user@yahoo.fr",
        "phone_number": "1234567890",
        "is_active": True,
        "role_name": "Gestion",
        "password": "password123",
    }

    user = controller.create_user(user_data)
    updated_data = {
        "username": "test_user_updated",
        "email": "test-update-user@gmail.com"
    }

    updated_user = controller.update_user(user.id, updated_data)
    assert updated_user.username == "test_user_updated"
    assert updated_user.email == "test-update-user@gmail.com"

def test_delete_user(db_session):
    """
    Test deleting a user
    input : db_session
    output : True
    """
    controller = UserController(db_session)
    user_data = {
        "id": str(uuid.uuid4()),
        "username": "test_user",
        "email": "test_user@hotmail.fr",
        "phone_number": "1234567890",
        "is_active": True,
        "role_name": "Gestion",
        "password": "password123",
    }
    user = controller.create_user(user_data)
    result = controller.delete_user(user.id)
    assert result is True

def test_get_all_support_users(db_session):
    """
    Test getting all support users
    input: db_session
    output: List of User objects
    """

    controller = UserController(db_session)

    support_user_data = {
        "id": str(uuid.uuid4()),
        "username": "support_user",
        "email": "support1@gmail.com",
        "phone_number": "1234567890",
        "is_active": True,
        "role_name": "Support",
        "password": "password123",
    }
    support_user = controller.create_user(support_user_data)
    support_users = controller.get_all_support_users()
    assert isinstance(support_users, list)

def test_get_all_commercial_users(db_session):
    """
    Test getting all commercial users
    input: db_session
    output: List of User objects
    """

    controller = UserController(db_session)
    commercial_user_data = {
        "id": str(uuid.uuid4()),
        "username": "commercial_user",
        "email": "commercial1@gmail.com",
        "phone_number": "1234567890",
        "is_active": True,
        "role_name": "Commercial",
        "password": "password123",
    }
    commercial_user = controller.create_user(commercial_user_data)
    commercial_users = controller.get_all_commercial_users()
    assert isinstance(commercial_users, list)