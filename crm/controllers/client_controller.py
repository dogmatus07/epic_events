from crm.models.models import Client
from crm.db.session import SessionLocal

class ClientController:
    """
    Controller class for Client model.
    """
    
    @staticmethod
    def get_all_clients():
        """
        Get all clients from the database.
        """
        db = SessionLocal()
        clients = db.query(Client).all()
        db.close()
        return clients

    @staticmethod
    def create_client(email, full_name, phone, company_name, first_contact_date, last_update_date, commercial_id):
        """
        Create a new client.
        """
        db = SessionLocal()
        client = Client(
            email=email,
            full_name=full_name,
            phone=phone,
            company_name=company_name,
            first_contact_date=first_contact_date,
            last_update_date=last_update_date,
            commercial_id=commercial_id
        )
        db.add(client)
        db.commit()
        db.close()
        return client
    
    @staticmethod
    def update_client(client_id, email, full_name, phone, company_name, first_contact_date, last_update_date, commercial_id):
        """
        Update a client.
        """
        db = SessionLocal()
        client = db.query(Client).filter(Client.id == client_id).first()
        client.email = email
        client.full_name = full_name
        client.phone = phone
        client.company_name = company_name
        client.first_contact_date = first_contact_date
        client.last_update_date = last_update_date
        client.commercial_id = commercial_id
        db.commit()
        db.close()
        return client
    
    @staticmethod
    def delete_client(client_id):
        """
        Delete a client.
        """
        db = SessionLocal()
        client = db.query(Client).filter(Client.id == client_id).first()
        db.delete(client)
        db.commit()
        db.close()
        return client
    