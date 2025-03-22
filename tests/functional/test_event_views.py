import pytest
from crm.views.event_views import create_event


def test_create_event_view(db_session, test_client, monkeypatch, setup_db):
    """
    Test create_event view
    """
    prompt_inputs = iter([
        "",               # Push enter to continue
        "1",              # Choose to edit a contract
        "1",              # Choose a contract by ID
        "1",              # Choose a support user
        "01-05-2025",     # Date start
        "06-05-2025",     # Date end
        "Paris",          # Location
        "100",            # attendees
        "Annual meeting with NGO",  # Notes
    ])

    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_inputs))

    event = create_event(db_session)

    assert event is not None
    assert event["location"] == "Paris"
    assert event["attendees"] == 100
