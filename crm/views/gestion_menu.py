from rich.console import Console
from rich.table import Table

console = Console()


def gestion_menu():
    """
    Display the main menu for the gestion role
    """
    while True:
        table = Table(
            title="Menu Gestion",
            show_header=True,
            show_lines=True,
            show_edge=False,
            header_style="bold magenta",
        )
        table.add_column("Option", style="dim")
        table.add_column("Description", justify="left")
        
        table.add_row("1", "Gérer les collaborateurs")
        table.add_row("2", "Gérer les contrats")
        table.add_row("3", "Gérer les clients")
        table.add_row("4", "Gérer les événements")
        table.add_row("5", "Retour au menu principal")
        
        console.print(table)
        
        choice = input("Entrez votre choix: ")
        if choice == "1":
            manage_collaborators()
        elif choice == "2":
            manage_contracts()
        elif choice == "3":
            manage_clients()
        elif choice == "4":
            manage_events()
        elif choice == "5":
            console.print("Retour au menu principal...", style="bold green")
            break
        else:
            console.print("Choix invalide, veuillez réessayer", style="bold red")


def manage_collaborators():
    """
    Manage collaborators
    """
    pass


def manage_contracts():
    """
    Manage contracts
    """
    pass


def manage_clients():
    """
    Manage clients
    """
    pass


def manage_events():
    """
    Manage events
    """
    pass
