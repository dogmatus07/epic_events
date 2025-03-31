import pytest
import uuid
from datetime import datetime, date
from crm.views.event_views import create_event, display_events_list, update_event, delete_event
from crm.views import event_views
from crm.controllers import EventController
from crm.models.models import Role


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

def test_display_event_list_view(db_session, test_client, monkeypatch, setup_db):
    """
    Test display_event_list view
    """
    prompt_inputs = iter([
        "",               # Push enter to continue
        "1",              # Choose to display all events
    ])

    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_inputs))

    # create a fake event
    event_controller = EventController(db_session)
    event_data = {
        "contract_id": "1",
        "event_date_start": datetime.strptime("21-03-2025", "%d-%m-%Y").date(),
        "event_date_end": datetime.strptime("27-03-2025", "%d-%m-%Y").date(),
        "location": "Paris",
        "attendees": 100,
        "notes": "Annual meeting with NGO",
        "support_id": "1"
    }
    event = event_controller.create_event(event_data)
    event_list = event_controller.get_events(db_session, support_only=False)
    display_events_list(event_list)
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: "")

    assert True

def test_select_event_view(db_session, test_client, monkeypatch, setup_db):
    """
    Test select_event view
    """
    prompt_values = iter([
        "1",  # Choose an event
        "1",  # Choose an event by ID
    ])

    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_values))

    assert True

def test_update_event_view(db_session, test_client, monkeypatch, setup_db):
    """
    Test update_event view
    input: event, db_session, is_support_user=False
    output: updated event data
    """

    # create a fake event for the test
    event_controller = EventController(db_session)

    event_data = {
        "contract_id": setup_db["contract"].id,
        "event_date_start": datetime.strptime("21-03-2025", "%d-%m-%Y").date(),
        "event_date_end": datetime.strptime("27-03-2025", "%d-%m-%Y").date(),
        "location": "Paris",
        "attendees": 100,
        "notes": "Annual meeting with NGO",
        "support_id": setup_db["user"].id
    }

    event = event_controller.create_event(event_data)

    # Update Phase
    prompt_inputs_update = iter([
        "01-05-2025",     # Date start
        "06-05-2025",     # Date end
        "Nancy",          # Location
        "130",            # attendees
        "Annual meeting with NGO",  # Notes
    ])

    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_inputs_update))
    monkeypatch.setattr("rich.prompt.Confirm.ask", lambda *args, **kwargs: True)


    updated_data = update_event(event, db_session, is_support_user=True)

    assert updated_data is not None
    assert updated_data["location"] == "Nancy"
    assert updated_data["attendees"] == 130

def test_delete_event_view(monkeypatch, db_session):
    """
    Test delete_event view
    """

    controller = EventController(db_session)

    # create a fake event
    event_data = {
        "contract_id": str(uuid.uuid4()),
        "event_date_start": datetime.strptime("21-03-2025", "%d-%m-%Y").date(),
        "event_date_end": datetime.strptime("27-03-2025", "%d-%m-%Y").date(),
        "location": "Paris",
        "attendees": 100,
        "notes": "Annual meeting with NGO",
        "support_id": str(uuid.uuid4())
    }
    event = controller.create_event(event_data)
    event_list = controller.get_events(db_session, support_only=False)
    prompt_value = iter([
        "",  # enter key to continue
        "1",  # select event menu
        "1",  # select event index
        "y",  # confirm deletion
        "",
    ])
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_value))
    monkeypatch.setattr("rich.prompt.Confirm.ask", lambda *args, **kwargs: True)
    result = delete_event(event, db_session)
    db_session.expire_all()
    remaining_events = controller.get_events(db_session, support_only=False)
    assert result is True
    assert len(remaining_events) == 0
