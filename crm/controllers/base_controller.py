import jwt
from crm.models.models import User
from sqlalchemy.orm import Session
from auth.auth_manager import SECRET_KEY


class BaseController:
    """
    Base controller class
    """

    def __init__(self, db_session: Session, current_user_token: str):
        self.db_session = db_session
        self.current_user = self.get_current_user(current_user_token)

    def get_current_user(self):
        """
        Get the current loged in user based on the token
        """
        try:
            payload = jwt.decode(current_user_token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            return self.db_session.query(User).get(user_id)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            print(e)
            return None
