import pytest
from crm.views.user_views import create_user


def test_create_user_view(db_session, monkeypatch, setup_db):
    """
    Test create_user view
    """
    prompt_values = iter([
        "JohnDoe",              # Nom d'utilisateur
        "johndoe@example.com",  # Email
        "0687909867",           # Téléphone
        "1",                    # Rôle
        "password123",          # Mot de passe
    ])

    input_values = iter([
        "y",                    # is_active (Confirm.ask)
        "",                     # Appui Entrée
    ])

    # All Prompt.ask
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_values))

    # Confirm.ask
    monkeypatch.setattr("rich.prompt.Confirm.ask", lambda *args, **kwargs: next(input_values).lower() in ["y", "yes"])

    user_data = create_user(db_session)

    assert isinstance(user_data, dict)
    assert user_data["username"] == "JohnDoe"
    assert user_data["email"] == "johndoe@example.com"
    assert user_data["phone_number"] == "0687909867"
    assert user_data["is_active"] is True
    assert user_data["role_name"] == "Gestion"
    assert user_data["password"] == "password123"
