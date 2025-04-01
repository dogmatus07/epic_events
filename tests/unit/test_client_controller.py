import pytest
from crm.controllers.client_controller import ClientController
from crm.models.models import Client
from datetime import datetime, date


def test_create_client(db_session):
    controller = ClientController(db_session)
    client_data = {
        "full_name": "Jane Doe",
        "email": "janedoe@gmail.com",
        "phone": "078654323",
        "company_name": "NEWCOMPANY LLC",
        "first_contact_date": datetime.now(),
        "last_update_date": datetime.now(),
    }
    client = controller.create_client(client_data)
    assert isinstance(client, Client)
    assert client.full_name == "Jane Doe"
    assert client.email == "janedoe@gmail.com"


def test_get_all_clients(db_session):
    controller = ClientController(db_session)
    clients = controller.get_all_clients()
    assert isinstance(clients, list)


def test_update_client(db_session):
    controller = ClientController(db_session)
    client_data = {
        "full_name": "Jane Doe",
        "email": "janedoe@gmail.com",
        "phone": "078654323",
        "company_name": "OldCompany",
        "first_contact_date": datetime.now(),
        "last_update_date": datetime.now(),
    }
    client = controller.create_client(client_data)

    updated_data = {"company_name": "NEWCOMPANY LTD"}
    updated_client = controller.update_client(client.id, updated_data)
    assert updated_client.company_name == "NEWCOMPANY LTD"
    assert isinstance(updated_client.last_update_date, date)


def test_delete_client(db_session):
    controller = ClientController(db_session)
    client = controller.create_client(
        {
            "full_name": "Jane Doe",
            "email": "janedoe@gmail.com",
            "phone": "078654323",
            "company_name": "NEWCOMPANY LTD",
            "first_contact_date": datetime.now(),
            "last_update_date": datetime.now(),
        }
    )
    result = controller.delete_client(client.id)
    assert result is True
