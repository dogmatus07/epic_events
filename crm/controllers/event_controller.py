from crm.models.models import Event
from crm.db.session import SessionLocal


class EventController:
    """
    Controller class for Event model.
    """

    @staticmethod
    def get_all_events():
        """
        Get all events from the database.
        """
        db = SessionLocal()
        events = db.query(Event).all()
        db.close()
        return events

    @staticmethod
    def create_event(
        contract_id,
        event_date_start,
        event_date_end,
        location,
        attendees,
        notes,
        support_id,
    ):
        """
        Create a new event.
        """

        db = SessionLocal()
        event = Event(
            contract_id=contract_id,
            event_date_start=event_date_start,
            event_date_end=event_date_end,
            location=location,
            attendees=attendees,
            notes=notes,
            support_id=support_id,
        )
        db.add(event)
        db.commit()
        db.close()
        return event

    @staticmethod
    def update_event(
        event_id,
        contract_id,
        event_date_start,
        event_date_end,
        location,
        attendees,
        notes,
        support_id,
    ):
        """
        Update an event.
        """
        db = SessionLocal()
        event = db.query(Event).filter(Event.id == event_id).first()
        event.contract_id = contract_id
        event.event_date_start = event_date_start
        event.event_date_end = event_date_end
        event.location = location
        event.attendees = attendees
        event.notes = notes
        event.support_id = support_id
        db.commit()
        db.close()
        return event

    @staticmethod
    def delete_event(event_id):
        """
        Delete an event.
        """
        db = SessionLocal()
        event = db.query(Event).filter(Event.id == event_id).first()
        db.delete(event)
        db.commit()
        db.close()
        return event
