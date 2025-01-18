from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.spinner import Spinner
from crm.views import commercial_menu


console = Console()


def commercial_menu():
    """
    Display the menu for the commercial role
    """
    while True:
        table = Table(
            title="Menu Commercial",
            show_header=False,
            show_lines=True,
            show_edge=False,
            header_style="bold magenta",
        )
        table.add_column("Option", justify="center", style="cyan")
        table.add_column("Description", justify="left", style="white")

        table.add_row("1", "Créer un client")
        table.add_row("2", "Mettre à jour un client")
        table.add_row("3", "Gérer les contrats")
        table.add_row("4", "Créer un événement")
        table.add_row("5", "Retour au menu principal")

        console.print(table)

        choice = Prompt.ask("Entrez votre choix : ")

        if choice == "1":
            create_client()
        elif choice == "2":
            update_client()
        elif choice == "3":
            manage_contracts()
        elif choice == "4":
            create_event()
        elif choice == "5":
            console.print("Quitter...", style="bold green")
            break
        else:
            console.print("Choix invalide, veuillez réessayer", style="bold red")


def create_client():
    """
    Create a new client
    """
    pass


def update_client():
    """
    Update a client
    """
    pass


def manage_contracts():
    """
    Manage contracts
    """
    pass


def create_event():
    """
    Create an event
    """
    pass
