import pytest
from crm.views.user_views import create_user


def test_create_user_view(db_session, monkeypatch):
    """
    Test create_user view
    """
    inputs = iter(
        [
            "John Doe",
            "johndoe@example.com",
            "0123456789",
            "y",
            "Gestion",
            "123456",
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )
    user = create_user(db_session)
    assert user is not None
    assert user.full_name == "John Doe"
