import pytest
import uuid
from datetime import datetime, date
from crm.views.client_views import display_client_list, create_client, select_client, update_client, delete_client
from crm.controllers.client_controller import ClientController
from crm.models.models import Client


def test_create_client_view(monkeypatch, db_session):
    prompt_values = iter([
        "John Doe",             # full name
        "johndoe@gmail.com",    # email`
        "1234567890",           # phone
        "DOE LLC",              # company name
        "03-03-2025",           # first contact date
        "05-03-2025",          # last update date
    ])
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_values))

    # Mock BaseController for commercial user
    class FakeUser():
        def __init__(self):
            self.id = str(uuid.uuid4())
            self.role_name = "commercial"

    class FakeBaseController():
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
    first_client = client_controller.create_client({
        "full_name": "John Doe",
        "email": "johndoe@gmail.com",
        "phone": "1234567890",
        "company_name": "DOE LLC",
        "first_contact_date": datetime.strptime("03-03-2025", "%d-%m-%Y").date(),
        "last_update_date": datetime.strptime("04-03-2025", "%d-%m-%Y").date(),
        "commercial_id": str(uuid.uuid4())
    })

    second_client = client_controller.create_client({
        "full_name": "Jane Doe",
        "email": "janedoe@yahoo.fr",
        "phone": "0987654321",
        "company_name": "DOE & Co",
        "first_contact_date": datetime.strptime("03-03-2025", "%d-%m-%Y").date(),
        "last_update_date": datetime.strptime("09-03-2025", "%d-%m-%Y").date(),
        "commercial_id": str(uuid.uuid4())
    })

    clients = client_controller.get_all_clients()
    assert len(clients) == 2
    assert first_client in clients
    assert second_client in clients

    # mock display client list
    monkeypatch.setattr("crm.views.client_views.display_client_list", lambda *args: None)
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: "")
    display_client_list(clients)

