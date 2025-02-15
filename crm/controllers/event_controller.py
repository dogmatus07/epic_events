from sqlalchemy.orm import Session
from crm.models.models import Event, User
from rich.console import Console


console = Console()

class EventController:
    """
    Controller class for Event model.
    """

    def __init__(self, db_session: Session, current_user_id=None):
        self.db_session = db_session
        self.current_user_id = current_user_id

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
            if not current_user:
                return []
            return (
                self.db_session.query(Event)
                .filter(Event.support_id.is_(current_user.id))
                .all()
            )
        return self.db_session.query(Event).all()

    def get_unassigned_events(self, db_session):
        """
        Get all events that are not assigned to a support user
        """
        events = self.db_session.query(Event).filter(Event.support_id.is_(None)).all()
        return events

    def assign_support(self, event_id, support_id):
        """
        Assign a support user to an event
        :param event_id: int, event id
        :param support_id: int, support user id
        """
        event = self.db_session.query(Event).get(event_id)
        if event:
            event.support_id = support_id
            self.db_session.commit()

    def get_events(self, db_session, support_only=False):
        """
        Get all events or only events assigned to a support user
        """
        console.print("[bold yellow]DEBUG: Récupération des événements en cours...[/]")
        events = db_session.query(Event).all()
        if support_only:
            current_user = self.get_current_user()
            if not current_user:
                return []

            return (
                self.db_session.query(Event)
                .filter(Event.support_id.is_(current_user.id))
                .all()
            )
        return events

    def get_current_user(self):
        """
        Get the current user
        """
        if not self.current_user_id:
            return None
        return (
            self.db_session.query(User)
            .filter(str(User.id) == self.current_user_id)
            .first()
        )
