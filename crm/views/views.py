from auth.auth_manager import AuthManager
from crm.db.session import SessionLocal
from rich.prompt import Prompt
from rich.console import Console

console = Console()


def authenticate_user():
    """
    Authenticate a user before 
    """
    db_session = SessionLocal()
    auth_manager = AuthManager(db_session)
    
    console.print("Authentification requise", style="bold blue")
    email = Prompt.ask("Email", style="bold green")
    password = Prompt.ask("Mot de passe", style="bold green", password=True)
    
    token = auth_manager.authenticate(email, password)
    if token:
        console.print("Authentification réussie", style="bold green")
        return token
    else:
        console.print("Authentification échouée, veuillez réessayer", style="bold red")
        return None
    