from sqlalchemy.orm import Session
from crm.models.models import Client
from datetime import datetime
from sentry_sdk import capture_exception
from rich.console import Console


console = Console()

class ClientController:
    """
    Controller class for Client model.
    """


    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_clients(self):
        """
        Get all clients from the database.
        """
        try:
            return self.db_session.query(Client).all()
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de la récupération des clients")
            return None

    def create_client(self, client_data):
        """
        Create a new client and assign it to the current commercial user.
        """
        try:
            new_client = Client(**client_data)
            self.db_session.add(new_client)
            self.db_session.commit()
            return new_client
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de la création du client")
            return None

    def update_client(self, client_id, updated_data):
        """
        Update a client.
        """
        try:
            client = self.db_session.query(Client).filter_by(id=client_id).first()
            if not client:
                return None
            for key, value in updated_data.items():
                setattr(client, key, value)
            client.last_update_date = datetime.now()
            self.db_session.commit()
            return client
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de la mise à jour du client")
            return None


    def delete_client(self, client_id):
        """
        Delete a client.
        """
        try:
            client = self.db_session.get(Client, client_id)
            if not client:
                return None
            self.db_session.delete(client)
            self.db_session.commit()
            return True
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de la suppression du client")
            return None
