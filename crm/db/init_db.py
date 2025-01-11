from crm.db.base import Base
from crm.db.session import engine


def initialize_database():
    """
    Initialize the database
    """
    print("Création de la base de données...")
    Base.metadata.create_all(bind=engine)
    print("Base de données créée avec succès !")

if __name__ == "__main__":
    initialize_database()
