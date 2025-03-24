import pytest
import uuid
import jwt
from crm.controllers.base_controller import BaseController
from crm.models.models import User
from sqlalchemy.orm import Session
from auth.auth_manager import SECRET_KEY


def generate_valid_token(user_id):
    """
    Generate a valid token
    input: user_id
    output: token
    """
    payload = {"user_id": user_id}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def test_get_current_user(db_session):
    """
    Test get_current_user method
    input: db_session
    output: None
    """
    user = User(
        id=str(uuid.uuid4()),
        username="testuser",
        email="testuser@gmail.com",
        phone_number="1234567890",
        is_active=True,
        role_name="Gestion",
    )
    user.set_password("testpassword123")
    db_session.add(user)
    db_session.commit()
    token = generate_valid_token(user.id)
    controller = BaseController(db_session, token)
    assert controller.current_user == user

def test_get_current_user_invalid_token(db_session):
    """
    Test get_current_user method with invalid token
    input: db_session
    output: None
    """
    token = "invalid_token"
    controller = BaseController(db_session, token)
    assert controller.current_user is None