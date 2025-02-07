from crm.views.views import authenticate_user
from crm.views.main_menu import main_menu
from auth.auth_manager import AuthManager
from crm.db.session import SessionLocal
from crm.db.session import get_db_session

db_session = get_db_session()

if __name__ == "__main__":
    token = None
    while not token:
        token = authenticate_user()

    # check the role of the user
    db_session = SessionLocal()
    auth_manager = AuthManager(db_session)
    payload = auth_manager.verify_token(token)
    if not payload:
        print("Token invalide ou expiré")
        exit()

    role = payload.get("role")
    user_id = payload.get("user_id")
    if not role:
        print("Rôle non trouvé dans le token")
        exit()
    else:
        print(f"Connexion réussie, Rôle: {role}")

    # display menu according to the role
    main_menu(role, db_session, user_id)
