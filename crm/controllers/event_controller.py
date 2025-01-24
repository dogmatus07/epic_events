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

    def filter_events(self, support_only=False):
        """
        Filter events based on the fact that they are assigned to a support user or not
        :param support_only: boolean, show only events assigned to a loged in support user
        :return: list of filtered events
        """
        if support_only:
            current_user = self.get_current_user()
            return self.db_session.query(Event).filter(Event.support_id == current_user.id).all()
        return self.db_session.query(Event).all()
    def get_unassigned_events(self):
        pass

    def assign_support(self, id, id1):
        pass

    def get_events(self, support_only):
        pass
