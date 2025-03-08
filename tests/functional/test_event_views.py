import pytest
from crm.views.event_views import create_event


def test_create_event_view(db_session, test_client, monkeypatch):
    """
    Test create_event view
    """
    inputs = iter(
        [
            test_client.id,
            "01-01-2025",
            "05-01-2025",
            "Paris",
            "100",
            "Annual meeting with NGO",
            "n",
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )
    event = create_event(db_session)
    assert event is not None
    assert event.location == "Paris"