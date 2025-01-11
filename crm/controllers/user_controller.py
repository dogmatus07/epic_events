from crm.models.models import User
from crm.db.session import SessionLocal


class UserController:
    """
    Controller class for User model.
    """

    @staticmethod
    def get_all_users():
        """
        Get all users from the database.
        """
        db = SessionLocal()
        users = db.query(User).all()
        db.close()
        return users

    @staticmethod
    def create_user(username, email, phone_number, role_name):
        """
        Create a new user.
        """
        user = User(
            username=username,
            email=email,
            phone_number=phone_number,
            role_name=role_name,
        )
        db.add(user)
        db.commit()
        db.close()
        return user

    @staticmethod
    def update_user(user_id, username, email, phone_number, role_name):
        """
        Update a user.
        """
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        user.username = username
        user.email = email
        user.phone_number = phone_number
        user.role_name = role_name
        db.commit()
        db.close()
        return user

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user.
        """
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        db.delete(user)
        db.commit()
        db.close()
        return user
