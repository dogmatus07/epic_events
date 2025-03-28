from rich.console import Console
from crm.utils.console import clear_console
from rich.table import Table
from rich.panel import Panel
from rich.box import DOUBLE
from rich import box
from rich.prompt import Prompt
from auth.auth_manager import AuthManager
from crm.db.session import SessionLocal
from sentry_sdk import capture_exception, capture_message

console = Console()

LOGO = r"""[bold blue]

 __ __   __   __     __    ___ __   __ __      
|_ |__)|/    |_ \  /|_ |\ | | (_   /  |__)|\/| 
|__|   |\__  |__ \/ |__| \| | __)  \__| \ |  | 
                                               
[/bold blue]
"""


def authenticate_user():
    """
    Authenticate a user before
    """
    db_session = SessionLocal()
    auth_manager = AuthManager(db_session)
    clear_console()
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
    try:
        email = Prompt.ask("Email")
        password = Prompt.ask("Mot de passe", password=True)

        token = auth_manager.authenticate(email, password)
        if token:
            console.print("Authentification réussie", style="bold green")
            return token
        else:
            capture_message("Authentification échouée pour l'utilisateur : " + email, level="warning")
            console.print("Authentification échouée, veuillez réessayer", style="bold red")
            return None
    except Exception as auth_error:
        capture_exception(auth_error)
        console.print("Erreur d'authentification", style="bold red")
        return None


def display_menu(title, options):
    """
    Display menu with common styling
    :param title: menu title
    :param options: list of options
    """
    clear_console()

    table = Table(title=f"[bold blue]✨{title}✨[/]", box=box.ROUNDED)
    table.add_column("[bold green]Index[/]", style="bold magenta", width=6)
    table.add_column("[bold green]Description[/]")

    try:
        for keys, values in options.items():
            table.add_row(keys, values)

        console.print(Panel(table, title="🔧 EPIC EVENTS CRM", expand=False))
        choice = Prompt.ask("[bold cyan]Choisissez une option[/]", choices=options.keys())
        return str(choice)
    except Exception as e:
        capture_exception(e)
        console.print("Une erreur s'est produite, veuillez réessayer", style="bold red")
        return None
