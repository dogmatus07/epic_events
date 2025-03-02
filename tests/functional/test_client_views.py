import pytest
from crm.views.client_views import create_client


def test_create_client_view(db_session, monkeypatch):
    """
    Test create_client view
    """
    inputs = iter(
        [
            "John Doe",
            "johndoe@example.com",
            "0102030405",
            "Client Company",
            "01-01-2025",
            "01-02-2025",
            "1",
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )
    client = create_client(db_session)
    assert client is not None
    assert client.full_name == "John Doe"


