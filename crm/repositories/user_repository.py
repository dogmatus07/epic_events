from sqlalchemy.orm import Session
from crm.models.models import User
from utils.password_utils import PasswordUtils


class UserRepository:
    """
    UserRepository class to interact with the User model
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_by_email(self, email: str) -> User:
        """
        Get a user by email
        """
        return self.db_session.query(User).filter_by(email=email).first()

    def create_user(self, username: str, email: str, password: str, role_name: str):
        """
        Create a user with hashed password
        """
        hashed_password = PasswordUtils.hash_password(password)
        user = User(
            username=username,
            email=email,
            password=hashed_password,
            role_name=role_name,
        )
        self.db_session.add(user)
        self.db_session.commit()
        return user
