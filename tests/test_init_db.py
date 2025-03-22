from crm.db.init_db import create_role, create_user
from crm.models.models import Role, User


def test_create_role(db_session):
    create_role(db_session)
    roles = db_session.query(Role).all()
    role_names = [r.role_name for r in roles]
    assert "Gestion" in role_names
    assert "Commercial" in role_names
    assert "Support" in role_names


def test_create_user(db_session):
    create_role(db_session)
    create_user(db_session)
    users = db_session.query(User).all()
    assert len(users) >= 6
    usernames = [u.username for u in users]
    assert "admin1" in usernames
    assert "commercial1" in usernames
    assert "support1" in usernames
