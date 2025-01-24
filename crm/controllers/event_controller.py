from sqlalchemy.orm import Session
from crm.models.models import Event


class EventController:
    """
    Controller class for Event model.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_contracts(self):
        """
        Get all events from the database.
        """
        return self.db_session.query(Event).all()

    def create_event(self, event_data):
        """
        Create a new event.
        """
        new_event = Event(**event_data)
        self.db_session.add(new_event)
        self.db_session.commit()
        return new_event

    def update_event(self, event_id, updated_data):
        """
        Update an event.
        """
        event = self.db_session.query(Event).get(event_id)
        if not event:
            return None
        for key, value in updated_data.items():
            setattr(event, key, value)
        self.db_session.commit()

        return event

    def delete_event(self, event_id):
        """
        Delete an event.
        """
        event = self.db_session.query(Event).get(event_id)
        if not event:
            return None
        self.db_session.delete(event)
        self.db_session.commit()
        return True
