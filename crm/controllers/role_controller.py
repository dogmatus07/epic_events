from crm.models.models import Role
from crm.db.session import SessionLocal


class RoleController:
    """
    Controller class for Role model.
    """
    @staticmethod
    def get_all_roles():
        """
        Get all roles from the database.
        """
        db = SessionLocal()
        roles = db.query(Role).all()
        db.close()
        return roles
    
    
    @staticmethod
    def create_role(role_name):
        """
        Create a new role.
        """
        db = SessionLocal()
        role = Role(role_name=role_name)
        db.add(role)
        db.commit()
        db.close()
        return role
    
    
    @staticmethod
    def delete_role(role_id):
        """
        Delete a role.
        """
        db = SessionLocal()
        role = db.query(Role).filter(Role.id == role_id).first()
        db.delete(role)
        db.commit()
        db.close()
        return role
    
    
    @staticmethod
    def update_role(role_id, role_name):
        """
        Update a role.
        """
        db = SessionLocal()
        role = db.query(Role).filter(Role.id == role_id).first()
        role.role_name = role_name
        db.commit()
        db.close()
        return role
    