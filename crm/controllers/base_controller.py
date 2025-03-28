import jwt
from crm.models.models import User
from sqlalchemy.orm import Session
from auth.auth_manager import SECRET_KEY
from sentry_sdk import capture_exception
from rich.console import Console


console = Console()


class BaseController:
    """
    Base controller class
    """

    def __init__(self, db_session: Session, current_user_token: str):
        self.db_session = db_session
        self.current_user_token = current_user_token
        self.current_user = self.get_current_user()

    def get_current_user(self):
        """
        Get the current logged in user based on the token
        """
        try:
            payload = jwt.decode(
                self.current_user_token, SECRET_KEY, algorithms=["HS256"]
            )
            user_id = payload.get("user_id")
            return self.db_session.get(User, user_id)
        except jwt.ExpiredSignatureError as e:
            capture_exception(e)
            console.print("❌ Token expired")
            return None
        except jwt.InvalidTokenError as e:
            capture_exception(e)
            console.print("❌ Invalid token")
            return None
        except Exception as e:
            capture_exception(e)
            console.print("❌ Error getting current user")
            return None
