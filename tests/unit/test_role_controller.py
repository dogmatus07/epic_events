import pytest
from crm.controllers import RoleController
from crm.models.models import Role


def test_create_role(db_session):
    """
    Test creating a role
    input: db_session
    output: Role object
    """
    controller = RoleController(db_session)
    role_data = {"role_name": "admin"}
    role = controller.create_role(role_data.get("role_name"))
    assert role is not None
    assert isinstance(role, Role)
    assert role.role_name == "admin"

def test_get_all_roles(db_session):
    """
    Test getting all roles
    input: db_session
    output: list of Role objects
    """
    controller = RoleController(db_session)
    roles = controller.get_all_roles()
    assert isinstance(roles, list)
    assert all(isinstance(role, Role) for role in roles)

def test_delete_role(db_session):
    """
    Test deleting a role
    input: db_session
    output: boolean
    """
    controller = RoleController(db_session)
    role_data = {"role_name": "test role"}
    role = controller.create_role(role_data.get("role_name"))
    result = controller.delete_role(role.role_name)
    assert result is True