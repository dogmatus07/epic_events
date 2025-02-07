from sqlalchemy.orm import Session
from crm.models.models import User, Role
from utils.password_utils import PasswordUtils


class UserController:
    """
    Controller class for User model.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_users(self):
        """
        Get all users from the database.
        """
        return self.db_session.query(User).all()

    def get_users_by_role(self, role_name: str):
        """
        Get all users with a specific role.
        """
        return self.db_session.query(User).join(Role).filter(Role.role_name == role_name)

    def create_user(self, user_data: dict):
        """
        Create a new user.
        """
        # check if user already exist
        existing_user = self.db_session.query(User).filter_by(email=user_data.get('email'))
        if existing_user:
            return None

        hashed_password = PasswordUtils.hash_password(user_data.pop('password'))
        new_user = User(**user_data, password=hashed_password)
        self.db_session.add(new_user)
        self.db_session.commit()
        return new_user

    def update_user(self, user_id, updated_data: dict):
        """
        Update a user.
        """
        user = self.db_session.query(User).get(user_id)
        if not user:
            return None

        if "password" in updated_data:
            updated_data["hashed_password"] = PasswordUtils.hash_password(updated_data.pop("password"))

        for key, value in updated_data.items():
            setattr(user, key, value)

        self.db_session.commit()
        return user

    def delete_user(self, user_id):
        """
        Delete a user.
        """
        user = self.db_session.query(User).get(user_id)
        if not user:
            return False
        self.db_session.delete(user)
        self.db_session.commit()
        return True

    def get_all_support_users(self):
        """
        Get all support users from the database.
        """
        return self.db_session.query(User).filter(User.role_name == "Support").all()

    def get_all_commercial_users(self):
        """
        Get all commercial users from the database.
        """
        return self.db_session.query(User).filter(User.role_name == "Commercial")
