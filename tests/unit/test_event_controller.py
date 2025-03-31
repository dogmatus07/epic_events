import pytest
from datetime import datetime
from crm.controllers.event_controller import EventController


def test_create_event(db_session, test_contract):
    """
    Test create_event function
    input: db_session, test_contract
    output: new_event
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

def test_get_all_events(db_session):
    """
    Test get_all_events function
    input: db_session
    output: events
    """
    event_controller = EventController(db_session)
    events = event_controller.get_events(db_session)
    assert isinstance(events, list)

def test_update_event(db_session, test_event):
    """
    Test update_event function
    input: db_session, test_event
    output: updated_event
    """
    event_controller = EventController(db_session)
    updated_data = {
        "location": "London",
        "attendees": 50,
    }
    updated_event = event_controller.update_event(test_event.id, updated_data)
    assert updated_event.location == "London"
    assert updated_event.attendees == 50

def test_delete_event(db_session, test_event):
    """
    Test delete_event function
    """
    controller = EventController(db_session)
    event = controller.create_event({
        "contract_id": test_event.contract_id,
        "event_date_start": test_event.event_date_start,
        "event_date_end": test_event.event_date_end,
        "location": test_event.location,
        "attendees": test_event.attendees,
        "notes": test_event.notes,
        "support_id": test_event.support_id,
    })
    result = controller.delete_event(event.id)
    assert result is True

def test_filter_events(db_session):
    """
    Test filter_events function
    input: db_session
    output: events
    """
    event_controller = EventController(db_session)
    events = event_controller.filter_events(support_only=False)
    assert isinstance(events, list)

def test_get_unassigned_event(db_session):
    """
    Test get_unassigned_events function
    input: db_session
    output: events
    """
    controller = EventController(db_session)
    event = controller.create_event({
        "contract_id": 1,
        "event_date_start": datetime.now(),
        "event_date_end": datetime.now(),
        "location": "Paris",
        "attendees": 100,
        "notes": "Annual meeting with NGO",
        "support_id": None,
    })
    events = controller.get_unassigned_events(db_session)
    assert event in events

def test_assign_support(db_session, setup_db):
    """
    Test assign_support function
    input: db_session, setup_db
    output: assigned_event
    """
    controller = EventController(db_session)
    event = controller.create_event({
        "contract_id": 1,
        "event_date_start": datetime.now(),
        "event_date_end": datetime.now(),
        "location": "Paris",
        "attendees": 100,
        "notes": "Annual meeting with NGO",
        "support_id": None,
    })
    assigned_event = controller.assign_support(event.id, 1)
    assert int(assigned_event.support_id) == 1
    assert assigned_event.support_id is not None
