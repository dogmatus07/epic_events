import pytest
from datetime import datetime
from crm.controllers.client_controller import ClientController


def test_create_client(db_session, test_user):
    """
    Test create_client function
    """
    client_controller = ClientController(db_session)
    client_data = {
        "full_name": "John Doe",
        "email": "newclient@example.com",
        "phone": "067890543",
        "company_name": "New Client Company",
        "first_contact_date": datetime.strptime("01-01-2025", "%d-%m-%Y").date(),
        "last_update_date": datetime.strptime("03-01-2025", "%d-%m-%Y").date(),
        "commercial_id": test_user.id,
    }
    new_client = client_controller.create_client(client_data)
    assert new_client is not None
    assert new_client.full_name == "John Doe"


def test_get_client(db_session, test_client):
    """
    Test get_client function
    """
    client_controller = ClientController(db_session)
    clients = client_controller.get_all_clients()
    assert len(clients) == 1
    assert clients[0].full_name == "John Doe"


def test_update_client(db_session, test_client):
    """
    Test update_client function
    """
    client_controller = ClientController(db_session)
    update_data = {"full_name": "Jane Super Doe"}
    update_client = client_controller.update_client(test_client.id, update_data)
    assert update_client.full_name == "Jane Super Doe"
