from rich.console import Console
from crm.views.views import authenticate_user
from crm.utils.console import clear_console
from crm.views.main_menu import main_menu
from auth.auth_manager import AuthManager
from crm.db.session import SessionLocal
from crm.db.session import get_db_session
from crm.utils.sentry import init_sentry
from sentry_sdk import capture_exception

console = Console()

init_sentry()

try:
    db_session = get_db_session()
except Exception as e:
    capture_exception(e)
    print("Erreur de connexion à la base de données")
    exit()

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
        clear_console()
        print(f"Connexion réussie, Rôle: {role}")

    # display menu according to the role
    try:
        clear_console()
        main_menu(role, db_session, token, user_id)
    except Exception as e:
        capture_exception(e)
        print("Une erreur s'est produite, veuillez réessayer")
        exit()
