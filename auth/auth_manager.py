import datetime
import jwt
from sqlalchemy.orm import Session
from crm.repositories.user_repository import UserRepository
from utils.password_utils import PasswordUtils


SECRET_KEY = "a9d81395ab98ff1d43b630570de08ccb9bb258952708841110c892090a2493a9"


class AuthManager:
    """
    AuthManager class to manage authentication
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.user_repository = UserRepository(db_session)

    def authenticate(self, email: str, password: str):
        """
        Authenticate a user
        """
        user = self.user_repository.get_user_by_email(email)
        if not user:
            return None

        if not PasswordUtils.verify_password(password, user.hashed_password):
            return None

        # generate token
        token = jwt.encode(
            {
                "user_id": user.id,
                "role": user.role_name,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            },
            SECRET_KEY,
            algorithm="HS256",
        )
        return token

    def verify_token(self, token: str):
        """
        Check token validity
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
