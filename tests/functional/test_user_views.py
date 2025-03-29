import pytest
import uuid
from crm.views.user_views import create_user, display_user_list, select_user, update_user
from crm.controllers.user_controller import UserController
from crm.models.models import User


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

def test_display_user_list_view(db_session, setup_db, capsys):
    """
    Test display_user_list view
    """

    # Create a user
    user_data = {
        "id": str(uuid.uuid4()),
        "username": "JohnDoe",
        "email": "johndoe@gmail.com",
        "phone_number": "0687909867",
        "is_active": True,
        "role_name": "Gestion",
        "hashed_password": "password",
    }

    user = User(**user_data)
    db_session.add(user)
    db_session.commit()

    users = UserController(db_session).get_all_users()
    display_user_list(users)
    captured = capsys.readouterr()
    assert "JohnDoe" in captured.out

def test_select_user_view(db_session, setup_db, monkeypatch):
    """
    Test select_user view
    input: users, default_id=None
    output: selected user
    """
    # Create a user
    user_data = {
        "id": str(uuid.uuid4()),
        "username": "JohnDoe",
        "email": "johndoe@example.com",
        "phone_number": "0687909867",
        "is_active": True,
        "role_name": "Gestion",
        "hashed_password": "password",
    }

    user = User(**user_data)
    db_session.add(user)
    db_session.commit()

    users = UserController(db_session).get_all_users()
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: "1")
    selected_user = select_user(users)
    assert selected_user == users[0]

def test_update_user_view(db_session, setup_db, monkeypatch):
    """
    Test update_user view
    """
    user_data = {
        "id": str(uuid.uuid4()),
        "username": "JohnDoe",
        "email": "johndoe@example.com",
        "phone_number": "0687909867",
        "is_active": True,
        "role_name": "Gestion",
        "hashed_password": "password",
    }

    user = User(**user_data)
    db_session.add(user)
    db_session.commit()

    prompt_values = iter([
        "JaneDoe",              # Nom d'utilisateur
        "jane@gmail.com",       # Email
        "0687909867",           # Téléphone
        "y",                    # is_active (Confirm.ask)
        "1",                    # Role - Gestion
        ""
    ])

    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_values))
    monkeypatch.setattr("rich.prompt.Confirm.ask", lambda *args, **kwargs: next(prompt_values).lower() in ["y", "yes"])

    updated_user = update_user(user, db_session)

    assert updated_user["username"] == "JaneDoe"
