from sqlalchemy.orm import Session
from crm.models.models import Event, User
from rich.console import Console
from sentry_sdk import capture_exception
from sqlalchemy.exc import SQLAlchemyError


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
        try:
            new_event = Event(**event_data)
            self.db_session.add(new_event)
            self.db_session.commit()
            return new_event
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de la création de l'événement")
            return None

    def update_event(self, event_id, updated_data):
        """
        Update an event.
        """
        try:
            event = self.db_session.get(Event, event_id)
            if not event:
                return None
            for key, value in updated_data.items():
                setattr(event, key, value)
            self.db_session.commit()
            return event
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de la mise à jour de l'événement")
            return None

    def delete_event(self, event_id):
        """
        Delete an event.
        """
        try:
            event = self.db_session.get(Event, event_id)
            if not event:
                return None
            self.db_session.delete(event)
            self.db_session.commit()
            return True
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de la suppression de l'événement")
            return None

    def filter_events(self, support_only=False):
        """
        Filter events based on the fact that they are assigned to a support user or not
        :param support_only: boolean, show only events assigned to a loged in support user
        :return: list of filtered events
        """
        try:
            if support_only:
                current_user = self.get_current_user()
                if not current_user:
                    return []

                events = (
                    self.db_session.query(Event)
                    .filter(Event.support_id == current_user.id)
                    .all()
                )
                return events

            events = self.db_session.query(Event).all()
            return events
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors du filtrage des événements")
            return None

    def get_unassigned_events(self, db_session):
        """
        Get all events that are not assigned to a support user
        """
        try:
            events = (
                self.db_session.query(Event).filter(Event.support_id.is_(None)).all()
            )
            return events
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de la récupération des événements non assignés")
            return None

    def assign_support(self, event_id, support_id):
        """
        Assign a support user to an event
        :param event_id: int, event id
        :param support_id: int, support user id
        """
        try:
            event = self.db_session.get(Event, event_id)
            if event:
                event.support_id = support_id
                self.db_session.commit()
                return event
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de l'assignation du support")
            return None

    def get_events(self, db_session, support_only=False):
        """
        Get all events or only events assigned to a support user
        """
        try:
            if support_only:
                current_user = self.get_current_user()
                if not current_user:
                    return []
                events = (
                    self.db_session.query(Event)
                    .filter(Event.support_id == str(current_user.id))
                    .all()
                )
                return events

            events = db_session.query(Event).all()
            return events
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de la récupération des événements")
            return None

    def get_current_user(self):
        """
        Get the current user
        """
        try:
            if not str(self.current_user_id):
                console.print("[bold red]❌ Aucun utilisateur actuel trouvé[/]")
                return None

            user = (
                self.db_session.query(User)
                .filter(User.id == str(self.current_user_id))
                .first()
            )
            if user:
                return user
            else:
                console.print("[bold red]❌ Aucun utilisateur actuel trouvé[/]")
            return user
        except SQLAlchemyError as e:
            capture_exception(e)
            console.print("Erreur lors de la récupération de l'utilisateur actuel")
            return None
