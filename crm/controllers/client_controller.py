from sqlalchemy.orm import Session
from crm.models.models import Client
from datetime import datetime


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
        return self.db_session.query(Client).all()

    def create_client(self, client_data):
        """
        Create a new client and assign it to the current commercial user.
        """

        new_client = Client(**client_data)
        self.db_session.add(new_client)
        self.db_session.commit()
        return new_client

    def update_client(self, client_id, updated_data):
        """
        Update a client.
        """
        client = self.db_session.query(Client).filter_by(id=client_id).first()
        if not client:
            return None
        for key, value in updated_data.items():
            setattr(client, key, value)
        client.last_update_date = datetime.now()
        self.db_session.commit()

        return client

    def delete_client(self, client_id):
        """
        Delete a client.
        """
        client = self.db_session.query(Client).get(client_id)
        if not client:
            return None
        self.db_session.delete(client)
        self.db_session.commit()
        return True
