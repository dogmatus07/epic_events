import pytest
from crm.controllers.event_controller import EventController


def test_create_event(db_session, test_client):
    """
    Test create_event function
    """
    event_controller = EventController(db_session)
    event_data = {
        "client_id": test_client.id,
        "event_date_start": "01-01-2025",
        "event_date_end": "05-01-2025",
        "location": "Paris",
        "attendees": "100",
        "notes": "Annual meeting with NGO",
        "support_id": None,
    }
    new_event = event_controller.create_event(event_data)
    assert new_event is not None
    assert new_event.location == "Paris"
