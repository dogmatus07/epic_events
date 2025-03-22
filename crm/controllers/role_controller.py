from sqlalchemy.orm import Session
from crm.models.models import Role


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
        return self.db_session.query(Role).all()

    def create_role(self, role_name: str):
        """
        Create a new role.
        """
        existing_role = (
            self.db_session.query(Role).filter_by(role_name=role_name).first()
        )
        if existing_role:
            return None
        new_role = Role(role_name=role_name)
        self.db_session.add(new_role)
        self.db_session.commit()
        return new_role

    def delete_role(self, role_id: int):
        """
        Delete a role.
        """
        role = self.db_session.get(Role, role_id)
        if not role:
            return None
        self.db_session.delete(role)
        self.db_session.commit()
        return True
