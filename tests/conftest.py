import pytest
import sys
import os
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crm.db.base import Base
from crm.models.models import Role, User, Client, Contract, Event
from auth.auth_manager import AuthManager
from utils.password_utils import PasswordUtils

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db_session):
    """
    Create a test user with a valid role
    """
    role = db_session.query(Role).filter_by(role_name="Commercial").first()
    user = User(
        username="test_user",
        email="test@example.com",
        phone_number="0102030405",
        is_active=True,
        role_name=role.role_name,
        hashed_password=PasswordUtils.hash_password("password"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_client(db_session, test_user):
    """
    Create a test client
    """
    client = Client(
        full_name="John Doe",
        email="client@example.com",
        phone="0102030405",
        company_name="Client Company",
        first_contact_date=date(2025, 1, 1),
        last_update_date=date(2025, 2, 1),
        commercial_id=test_user.id,
    )
    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)
    return client

