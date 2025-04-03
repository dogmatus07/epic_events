import pytest
from auth.auth_manager import AuthManager


def test_authenticate_user(db_session, test_user):
    """
    Test user authentication.
    """
    auth_manager = AuthManager(db_session)
    token = auth_manager.authenticate(test_user.email, "password")
    assert token is not None


def test_authenticate_user_invalid_password(db_session, test_user):
    """
    Test user authentication with invalid password.
    """
    auth_manager = AuthManager(db_session)
    token = auth_manager.authenticate(test_user.email, "wrongpassword")
    assert token is None


def test_verify_valid_token(db_session, test_user):
    """
    Test token verification.
    """
    auth_manager = AuthManager(db_session)
    token = auth_manager.authenticate(test_user.email, "password")
    payload = auth_manager.verify_token(token)
    assert payload is not None
    assert payload["user_id"] == test_user.id
