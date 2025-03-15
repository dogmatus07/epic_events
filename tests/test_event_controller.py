import pytest
from datetime import datetime
from crm.controllers.event_controller import EventController


def test_create_event(db_session, test_contract):
    """
    Test create_event function
    """
    event_controller = EventController(db_session)
    event_data = {
        "contract_id": test_contract.id,
        "event_date_start": datetime.strptime("01-01-2025", "%d-%m-%Y"),
        "event_date_end": datetime.strptime("06-01-2025", "%d-%m-%Y"),
        "location": "Paris",
        "attendees": 100,
        "notes": "Annual meeting with NGO",
        "support_id": None,
    }
    new_event = event_controller.create_event(event_data)
    assert new_event is not None
    assert new_event.location == "Paris"
