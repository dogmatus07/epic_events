from sqlalchemy.orm import Session
from crm.models.models import User, Role
from utils.password_utils import PasswordUtils
from sentry_sdk import capture_exception
from rich.console import Console

console = Console()


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
        try:
            users_by_role = self.db_session.query(User).join(Role).filter(Role.role_name == role_name)
            if users_by_role:
                return users_by_role.all()
            else:
                return None
        except Exception as e:
            capture_exception(e)
            console.print("Error getting users by role")
            return None

    def create_user(self, user_data: dict):
        """
        Create a new user.
        """
        # check if user already exist
        try:
            self.db_session.expire_all()
            existing_user = self.db_session.query(User).filter_by(
                email=user_data.get("email")).first()
            if existing_user:
                return None

            password = user_data.get("password")
            if not password:
                return None

            hashed_password = PasswordUtils.hash_password(user_data.pop("password"))
            new_user = User(**user_data, hashed_password=hashed_password)
            self.db_session.add(new_user)
            self.db_session.commit()
            user_verif = self.db_session.query(User).filter_by(email=user_data["email"]).first()
            return new_user
        except Exception as e:
            capture_exception(e)
            console.print("Error creating user")
            return None

    def update_user(self, user_id, updated_data: dict):
        """
        Update a user.
        """
        try:
            user = self.db_session.get(User, user_id)
            if not user:
                return None

            if "password" in updated_data:
                updated_data["hashed_password"] = PasswordUtils.hash_password(
                    updated_data.pop("password")
                )

            for key, value in updated_data.items():
                setattr(user, key, value)

            self.db_session.commit()
            return user
        except Exception as e:
            capture_exception(e)
            console.print("Error updating user")
            return None

    def delete_user(self, user_id):
        """
        Delete a user.
        """
        try:
            user = self.db_session.get(User, user_id)
            if not user:
                return False
            self.db_session.delete(user)
            self.db_session.commit()
            return True
        except Exception as e:
            capture_exception(e)
            console.print("Error deleting user")
            return None

    def get_all_support_users(self):
        """
        Get all support users from the database.
        """
        try:
            all_support_users = self.db_session.query(User).filter(User.role_name == "Support").all()
            if all_support_users:
                return all_support_users
            else:
                return None
        except Exception as e:
            capture_exception(e)
            console.print("Error getting all support users")
            return None

    def get_all_commercial_users(self):
        """
        Get all commercial users from the database.
        """
        return self.db_session.query(User).filter(User.role_name == "Commercial").all()
