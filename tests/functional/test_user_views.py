import pytest
from crm.views.user_views import create_user
from crm.models.models import User


def test_create_user_view(db_session, monkeypatch, setup_db):
    """
    Test create_user view
    """
    inputs = iter(
        [
            "JohnDoe",
            "johndoe@example.com",
            "0123456789",
            "y",
            "Gestion",
            "123456",
            "",
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda *args: next(inputs),
    )
    monkeypatch.setattr(
        "rich.prompt.Prompt.ask",
        lambda *args, **kwargs: "1",
    )
    user = create_user(db_session)
    assert isinstance(user, User)
    assert user.username == "JohnDoe"
