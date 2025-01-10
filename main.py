from crm.db.base import Base
from crm.db.session import engine


if __name__ == '__main__':
    print('Création de la base de données...')
    Base.metadata.create_all(bind=engine)
    print('Base de données créée avec succès !')

