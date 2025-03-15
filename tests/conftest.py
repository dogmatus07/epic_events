import pytest
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crm.db.base import Base
from crm.models.models import Role, User, Client, Contract, Event
from auth.auth_manager import AuthManager
from utils.password_utils import PasswordUtils

# 🔹 Create a test database in memory
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a clean database for each test.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def setup_db(db_session):
    """
    Initialize the database with test data.
    """

    # 🔹 Add roles
    roles = [
        Role(role_name="Gestion"),
        Role(role_name="Commercial"),
        Role(role_name="Support"),
    ]
    db_session.add_all(roles)
    db_session.commit()

    # 🔹 Add commercial user
    test_user = User(
        id=str(uuid.uuid4()),
        username="test_user",
        email="test@example.com",
        phone_number="0102030405",
        is_active=True,
        role_name="Commercial",
        hashed_password=PasswordUtils.hash_password("password"),
    )
    db_session.add(test_user)
    db_session.commit()

    # 🔹 Add support user
    support_user = User(
        id=str(uuid.uuid4()),
        username="support_user",
        email="support@epicevents.com",
        phone_number="078976543",
        is_active=True,
        role_name="Support",
        hashed_password=PasswordUtils.hash_password("supportpassword"),
    )
    db_session.add(support_user)
    db_session.commit()


    # 🔹 Add client
    test_client = Client(
        id=str(uuid.uuid4()),
        full_name="John Doe",
        email="client@example.com",
        phone="0102030405",
        company_name="Client Company",
        first_contact_date=datetime.strptime("01-01-2025", "%d-%m-%Y").date(),
        last_update_date=datetime.strptime("01-02-2025", "%d-%m-%Y").date(),
        commercial_id=test_user.id,
    )
    db_session.add(test_client)
    db_session.commit()

    # 🔹 Add contract
    test_contract = Contract(
        id=str(uuid.uuid4()),
        client_id=test_client.id,
        total_amount=1000.0,
        amount_due=500.0,
        signed=True,
        commercial_id=test_user.id,
    )
    db_session.add(test_contract)
    db_session.commit()

    # 🔹 Add event
    test_event = Event(
        id=str(uuid.uuid4()),
        contract_id=test_contract.id,
        event_date_start=datetime(2025, 1, 1, 10, 0, 0),
        event_date_end=datetime(2025, 1, 5, 18, 0, 0),
        location="Paris",
        attendees=100,
        notes="Annual meeting with NGO",
        support_id=test_user.id,
    )
    db_session.add(test_event)
    db_session.commit()

    return {
        "user": test_user,
        "client": test_client,
        "contract": test_contract,
        "event": test_event,
    }


@pytest.fixture
def test_user(db_session, setup_db):
    """
    Get the test user.
    """
    return setup_db["user"]


@pytest.fixture
def test_client(db_session, setup_db):
    """
    Get the test client.
    """
    return setup_db["client"]


@pytest.fixture
def test_contract(db_session, setup_db):
    """
    Get the test contract.
    """
    return setup_db["contract"]


@pytest.fixture
def test_event(db_session, setup_db):
    """
    Get the test event.
    """
    return setup_db["event"]
