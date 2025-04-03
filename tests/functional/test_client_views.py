import pytest
import uuid
from datetime import datetime, date
from crm.views.client_views import (
    display_client_list,
    create_client,
    select_client,
    update_client,
    delete_client,
)
from crm.controllers.client_controller import ClientController
from crm.models.models import Client


def test_create_client_view(monkeypatch, db_session):
    prompt_values = iter(
        [
            "John Doe",  # full name
            "johndoe@gmail.com",  # email`
            "1234567890",  # phone
            "DOE LLC",  # company name
            "03-03-2025",  # first contact date
            "05-03-2025",  # last update date
        ]
    )
    monkeypatch.setattr(
        "rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_values)
    )

    # Mock BaseController for commercial user
    class FakeUser:
        def __init__(self):
            self.id = str(uuid.uuid4())
            self.role_name = "commercial"

    class FakeBaseController:
        def __init__(self, db_session, token):
            self.current_user = FakeUser()

    monkeypatch.setattr("crm.views.client_views.BaseController", FakeBaseController)

    current_user_token = "FAKE_TOKEN"
    client_data = create_client(db_session, current_user_token)
    assert client_data is not None
    assert client_data.full_name == "John Doe"
    assert client_data.email == "johndoe@gmail.com"


def test_display_client_list(monkeypatch, db_session):
    client_controller = ClientController(db_session)
    first_client = client_controller.create_client(
        {
            "full_name": "John Doe",
            "email": "johndoe@gmail.com",
            "phone": "1234567890",
            "company_name": "DOE LLC",
            "first_contact_date": datetime.strptime("03-03-2025", "%d-%m-%Y").date(),
            "last_update_date": datetime.strptime("04-03-2025", "%d-%m-%Y").date(),
            "commercial_id": str(uuid.uuid4()),
        }
    )

    second_client = client_controller.create_client(
        {
            "full_name": "Jane Doe",
            "email": "janedoe@yahoo.fr",
            "phone": "0987654321",
            "company_name": "DOE & Co",
            "first_contact_date": datetime.strptime("03-03-2025", "%d-%m-%Y").date(),
            "last_update_date": datetime.strptime("09-03-2025", "%d-%m-%Y").date(),
            "commercial_id": str(uuid.uuid4()),
        }
    )

    clients = client_controller.get_all_clients()
    assert len(clients) == 2
    assert first_client in clients
    assert second_client in clients

    # mock display client list
    monkeypatch.setattr(
        "crm.views.client_views.display_client_list", lambda *args: None
    )
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: "")
    display_client_list(clients)


def test_select_client_view(monkeypatch, db_session):
    """
    Test the select_client function to ensure it returns a client object based on user input.
    """

    controller = ClientController(db_session)

    first_client = controller.create_client(
        {
            "full_name": "John Doe",
            "email": "johndoe@gmail.com",
            "phone": "1234567890",
            "company_name": "DOE LLC",
            "first_contact_date": datetime.strptime("03-03-2025", "%d-%m-%Y").date(),
            "last_update_date": datetime.strptime("04-03-2025", "%d-%m-%Y").date(),
            "commercial_id": str(uuid.uuid4()),
        }
    )

    second_client = controller.create_client(
        {
            "full_name": "Jane Doe",
            "email": "janedoe@yahoo.fr",
            "phone": "0987654321",
            "company_name": "DOE & Co",
            "first_contact_date": datetime.strptime("03-03-2025", "%d-%m-%Y").date(),
            "last_update_date": datetime.strptime("09-03-2025", "%d-%m-%Y").date(),
            "commercial_id": str(uuid.uuid4()),
        }
    )

    clients = controller.get_all_clients()
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: "2")
    selected_client = select_client(clients)
    assert selected_client is not None
    assert selected_client.full_name == "Jane Doe"


def test_update_client_view(monkeypatch, db_session):
    """
    Test the update_client function to ensure it updates a client object based on user input.
    """

    controller = ClientController(db_session)

    client = controller.create_client(
        {
            "id": str(uuid.uuid4()),
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "phone": "1234567890",
            "company_name": "Doe Enterprises",
            "first_contact_date": datetime.strptime("01-01-2025", "%d-%m-%Y").date(),
            "last_update_date": datetime.strptime("01-02-2025", "%d-%m-%Y").date(),
            "commercial_id": str(uuid.uuid4()),
        }
    )

    monkeypatch.setattr("crm.views.client_views.select_client", lambda x: client)

    inputs = iter(
        [
            "Jane Smith",  # full name
            "janesmith@gmail.com",  # email
            "0987654321",  # phone
            "Smith LLC",  # company name
            "03-03-2025",  # first contact date
            "05-03-2025",  # last update date
        ]
    )
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(inputs))
    updated_client = update_client(db_session)

    assert updated_client is not None
    assert updated_client.full_name == "Jane Smith"
    assert updated_client.email == "janesmith@gmail.com"
    assert updated_client.phone == "0987654321"


def test_delete_client_views(monkeypatch, db_session):
    """
    Test the delete_client function to ensure it deletes a client object based on user input.
    """

    controller = ClientController(db_session)

    # create a fake client
    client_data = {
        "full_name": "John Doe",
        "email": "johndoe@laposte.net",
        "phone": "1234567890",
        "company_name": "Doe Enterprises",
        "first_contact_date": datetime.strptime("01-01-2025", "%d-%m-%Y").date(),
        "last_update_date": datetime.strptime("01-02-2025", "%d-%m-%Y").date(),
        "commercial_id": str(uuid.uuid4()),
    }

    client = controller.create_client(client_data)

    prompt_value = iter(
        [
            "",  # enter key to continue
            "1",  # select client menu
            "1",  # select client index
            "y",  # confirm deletion
            "",  # enter key to continue
        ]
    )

    monkeypatch.setattr(
        "rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_value)
    )
    monkeypatch.setattr("rich.prompt.Confirm.ask", lambda *args, **kwargs: True)

    delete_client(db_session)
    clients = controller.get_all_clients()
    assert client not in clients
    assert len(clients) == 0
