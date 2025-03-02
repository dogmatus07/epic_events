import pytest
from auth.auth_manager import AuthManager


def test_authenticate_user(db_session, test_user):
    """
    Test authenticate_user function
    """
    auth_manager = AuthManager(db_session)
    token = auth_manager.authenticate(test_user.email, "testpassword")
    assert token is not None


def test_authenticate_user_invalid_password(db_session, test_user):
    """
    Test authenticate_user function with invalid password
    """
    auth_manager = AuthManager(db_session)
    token = auth_manager.authenticate(test_user.email, "invalidpassword")
    assert token is None


def test_verify_valid_token(db_session, test_user):
    """
    Test verify_token function with a valid token
    """
    auth_manager = AuthManager(db_session)
    token = auth_manager.authenticate(test_user.email, "testpassword")
    payload = auth_manager.verify_token(token)
    assert payload is not None
    assert payload["user_id"] == test_user.id


def test_verify_invalid_token(db_session):
    """
    Test verify_token function with an invalid token
    """
    auth_manager = AuthManager(db_session)
    payload = auth_manager.verify_token("invalid.token")
    assert payload is None
