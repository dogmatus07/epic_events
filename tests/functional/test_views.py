import pytest
from rich.prompt import Prompt
from crm.views.views import authenticate_user, display_menu
from auth.auth_manager import AuthManager


def test_authenticate_user_view(monkeypatch, mocker):
    """
    Test the authenticate_user view
    """

    # Mock the Prompt.ask function
    prompt_values = iter(["test@example.com", "password"])
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_values))

    # mock SessionLocal
    mock_db_session = mocker.Mock()
    mock_session_local = mocker.patch("crm.views.views.SessionLocal", return_value=mock_db_session)


    # Mock the AuthManager.authenticate function
    mock_auth_manager = mocker.patch("crm.views.views.AuthManager")
    mock_auth_instance = mock_auth_manager.return_value
    mock_auth_instance.authenticate.return_value = "FAKE TOKEN"

    token = authenticate_user()
    assert token == "FAKE TOKEN"

def test_display_menu_view(monkeypatch, mocker):
    """
    Test the display_menu view
    """

    # Mock the Prompt.ask function
    prompt_values = iter(["1"])
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_values))

    # Mock the console object
    mock_console = mocker.Mock()
    mock_console.print = mocker.Mock()
    mock_console.clear = mocker.Mock()
    mock_console.print.return_value = None
    mock_console.clear.return_value = None

    # Mock the console object
    mock_console = mocker.Mock()
    mock_console.print = mocker.Mock()
    mock_console.clear = mocker.Mock()
    mock_console.print.return_value = None
    mock_console.clear.return_value = None

    # Mock the display_menu function
    mock_display_menu = mocker.patch("crm.views.views.display_menu")
    mock_display_menu.return_value = None

    options = {
        "1": "Option 1",
        "2": "Option 2",
    }

    choice = display_menu("Test Menu", options)
    assert choice == "1"
