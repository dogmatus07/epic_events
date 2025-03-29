from sqlalchemy.orm import Session
from crm.models.models import Role
from sentry_sdk import capture_exception
from rich.console import Console


console = Console()


class RoleController:
    """
    Controller class for Role model.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_roles(self):
        """
        Get all roles from the database.
        """

        try:
            return self.db_session.query(Role).all()
        except Exception as e:
            capture_exception(e)
            console.print("Error getting all roles")
            return None

    def create_role(self, role_name: str):
        """
        Create a new role.
        """
        try:
            existing_role = (
                self.db_session.query(Role).filter_by(role_name=role_name).first()
            )
            if existing_role:
                return None
            new_role = Role(role_name=role_name)
            self.db_session.add(new_role)
            self.db_session.commit()
            return new_role
        except Exception as e:
            capture_exception(e)
            console.print("Error creating role")
            return None

    def delete_role(self, role_id: int):
        """
        Delete a role.
        """
        try:
            role = self.db_session.get(Role, role_id)
            if not role:
                return None
            self.db_session.delete(role)
            self.db_session.commit()
            return True
        except Exception as e:
            capture_exception(e)
            console.print("Error deleting role")
            return None
