from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from crm.views.gestion_menu import gestion_menu
from crm.views.commercial_menu import commercial_menu
from crm.views.support_menu import support_menu


console = Console()


def main_menu(role):
    """
    Main menu redirecting to the right menu based on roles
    """
    table = Table(
        title="Menu Principal",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Option", justify="center", style="cyan")
    table.add_column("Description", justify="left", style="white")

    if role == "Gestion":
        table.add_row("1", "Menu Gestion")
    elif role == "Commercial":
        table.add_row("1", "Menu Commercial")
    elif role == "Support":
        table.add_row("1", "Menu Support")
    else:
        console.print("Rôle invalide", style="bold red")
        return

    table.add_row("0", "Quitter")
    console.print(table)

    choice = Prompt.ask("Entrez votre choix : ")

    if choice == "1":
        if role == "Gestion":
            gestion_menu()
        elif role == "Commercial":
            commercial_menu()
        elif role == "Support":
            support_menu()
    elif choice == "0":
        console.print("Fermeture de l'application...", style="bold green")
    else:
        console.print("Choix invalide, veuillez réessayer", style="bold red")
