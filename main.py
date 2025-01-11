from views.views import authenticate_user, main_menu
from auth.auth_manager import AuthManager
from crm.db.session import SessionLocal



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
    
    role = payload["role"]
    print("Connexion réussie en tant que", role)
    
    # display menu according to the role
    main_menu(role)
