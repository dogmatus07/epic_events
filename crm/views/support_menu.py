from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.spinner import Spinner


console = Console()


def support_menu():
    """
    Display the menu for the support role
    """
    while True:
        table = Table(
            title="Menu Support",
            show_header=False,
            show_lines=True,
            show_edge=False,
            box=box.SIMPLE,
            header_style="bold magenta",
        )
        table.add_column("Option", justify="center", style="cyan")
        table.add_column("Description", justify="left", style="white")
        
        table.add_row("1", "Lister mes événements")
        table.add_row("2", "Mettre à jour un événement")
        table.add_row("3", "Retour au menu principal")
        
        console.print(table)
        
        choice = Prompt.ask("Entrez votre choix : ")
        
        if choice == "1":
            list_my_events()
        elif choice == "2":
            update_my_event()
        elif choice == "3":
            console.print("Retour au menu principal...", style="bold green")
            break
        else:
            console.print("Choix invalide, veuillez réessayer", style="bold red")


def list_my_events():
    """
    List all events
    """
    pass


def update_my_event():
    """
    Update an event
    """
    pass
