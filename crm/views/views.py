import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import DOUBLE
from rich.prompt import Prompt, Confirm
from auth.auth_manager import AuthManager
from crm.db.session import SessionLocal

console = Console()

LOGO = """[bold blue]

 __ __   __   __     __    ___ __   __ __      
|_ |__)|/    |_ \  /|_ |\ | | (_   /  |__)|\/| 
|__|   |\__  |__ \/ |__| \| | __)  \__| \ |  | 
                                               
[/bold blue]
"""


def clear_screen():
    """
    Clear the screen
    """
    os.system("cls" if os.name == "nt" else "clear")


def authenticate_user():
    """
    Authenticate a user before
    """
    db_session = SessionLocal()
    auth_manager = AuthManager(db_session)
    console.clear()
    console.print(LOGO)
    console.print(
        Panel.fit(
            "[bold blue]Bienvenue dans Epic Events CRM[/]\n"
            "[bold yellow] Veuillez vous connecter pour continuer[/]\n",
            title="[bold magenta]Authentification[/]",
            border_style="bright_magenta",
            box=DOUBLE,
        )
    )
    email = Prompt.ask("Email")
    password = Prompt.ask("Mot de passe", password=True)

    token = auth_manager.authenticate(email, password)
    if token:
        console.print("Authentification réussie", style="bold green")
        return token
    else:
        console.print("Authentification échouée, veuillez réessayer", style="bold red")
        return None
