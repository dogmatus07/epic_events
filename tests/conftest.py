import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crm.db.base import Base
from crm.models.models import Role, User, Client, Contract, Event
from auth.auth_manager import AuthManager
from utils.password_utils import PasswordUtils

# Create a SQLite database in memory
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a new database session for a test
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    # adding default roles
    role_gestion = Role(role_name="Gestion")
    role_commercial = Role(role_name="Commercial")
    role_support = Role(role_name="Support")

    session.add_all([role_gestion, role_commercial, role_support])
    session.commit()

    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db_session):
    """
    Create a test user
    """
    user = User(
        username="test_user",
        email="test@example.com",
        phone_number="0102030405",
        is_active=True,
        role_name="Commercial",
        hashed_password=PasswordUtils.hash_password("password"),
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_client(db_session):
    """
    Create a test client
    """
    client = Client(
        full_name="John Doe",
        email="client@example.com",
        phone="0102030405",
        company_name="Client Company",
        first_contact_date="01-01-2025",
        last_update_date="01-02-2025",
        commercial_id=test_user.id,
    )
    db_session.add(client)
    db_session.commit()
    return client

