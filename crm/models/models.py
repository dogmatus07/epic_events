import uuid
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Boolean,
    Date,
    Float,
    DateTime,
    Integer,
)
from sqlalchemy.orm import relationship
from crm.db.base import Base
from passlib.hash import bcrypt


class Role(Base):
    """
    User Role model
    """

    __tablename__ = "roles"
    role_name = Column(String, primary_key=True)
    users = relationship("User", back_populates="role")


class User(Base):
    """
    User model
    """

    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(15), unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    role_name = Column(String, ForeignKey("roles.role_name"))
    hashed_password = Column(String, nullable=False)

    role = relationship("Role", back_populates="users")
    clients = relationship("Client", back_populates="commercial")
    contracts = relationship("Contract", back_populates="commercial")
    events = relationship("Event", back_populates="support_contact")
    
    
    def set_password(self, password: str):
        """
        Set the password for the user
        """
        self.hashed_password = bcrypt.hash(password)
    
    
    def verify_password(self, password: str) -> bool:
        """
        Verify the password for the user
        """
        return bcrypt.verify(password, self.hashed_password)
        


class Client(Base):
    """
    Client model
    """

    __tablename__ = "clients"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=True)
    company_name = Column(String(50), nullable=False)
    first_contact_date = Column(Date, nullable=False)
    last_update_date = Column(Date, nullable=False)

    commercial_id = Column(String, ForeignKey("users.id"))
    commercial = relationship("User", back_populates="clients")
    contracts = relationship("Contract", back_populates="client")


class Contract(Base):
    """
    Contract model
    """

    __tablename__ = "contracts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"))
    total_amount = Column(Float, nullable=False)
    amount_due = Column(Float, nullable=False)
    signed = Column(Boolean, default=False)

    commercial_id = Column(String, ForeignKey("users.id"))
    commercial = relationship("User", back_populates="contracts")
    client = relationship("Client", back_populates="contracts")
    events = relationship("Event", back_populates="contract")


class Event(Base):
    """
    Event model
    """

    __tablename__ = "events"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    contract_id = Column(String, ForeignKey("contracts.id"))
    event_date_start = Column(DateTime, nullable=False)
    event_date_end = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)

    support_id = Column(String, ForeignKey("users.id"))
    support_contact = relationship("User", back_populates="events")
    contract = relationship("Contract", back_populates="events")
