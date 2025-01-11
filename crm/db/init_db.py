import uuid
from datetime import datetime
from crm.db.base import Base
from crm.db.session import engine, SessionLocal
from crm.models.models import (
    Role,
    User,
    Client,
    Contract,
    Event
)


def create_role(session):
    """
    Create the roles
    """
    roles = ["Gestion", "Commercial", "Support"]
    for role_name in roles:
        role = Role(role_name=role_name)
        session.add(role)
    session.commit()
    print("Roles créés avec succès !")


def create_user(session):
    """
    Create users
    """
    users = [
        # gestion users
        User(
            id=uuid.uuid4(),
            username="admin1",
            email="admin1@epicevents.com",
            phone_number="065849785",
            is_active=True,
            role_name="Gestion"            
        ),
        User(
            id=uuid.uuid4(),
            username="admin2",
            email="admin2@epicevents.com",
            phone_number="065123496",
            is_active=True,
            role_name="Gestion"
        ),
        
        # commercial users
        User(
            id=uuid.uuid4(),
            username="commercial1",
            email="commercial1@epicevents.com",
            phone_number="069963214",
            is_active=True,
            role_name="Commercial"
        ),
        User(
            id=uuid.uuid4(),
            username="commercial2",
            email="commercial2@epicevents.com",
            phone_number="064425816",
            is_active=True,
            role_name="Commercial"
        ),
        
        # support users
        User(
            id=uuid.uuid4(),
            username="support1",
            email="support1@epicevents.com",
            phone_number="067784695",
            is_active=True,
            role_name="Support"
        ),
        User(
            id=uuid.uuid4(),
            username="support2",
            email="support2@epicevents.com",
            phone_number="061125694",
            is_active=True,
            role_name="Support"
        )
    ]
    
    # set default passowrds
    for user in users:
        user.set_password("epic-evenTs2025")
    
    session.add_all(users)
    session.commit()
    print("Utilisateurs créés avec succès !")


def initialize_database():
    """
    Initialize the database
    """
    print("Création de la base de données...")
    Base.metadata.create_all(bind=engine)
    print("Base de données créée avec succès !")

if __name__ == "__main__":
    initialize_database()
