from rich.console import Console
from rich.table import Table
from rich.box import box
from rich.spinner import Spinner

console = Console()

def processing_task():
    """
    Display a spinner while processing a task
    """
    spinner = Spinner("dots", text="Traitement en cours...")
    console.print(spinner, end="\r")
    time.sleep(3)
    console.print("Traitement terminé", style="bold green")

def gestion_menu():
    """
    Display the main menu for the gestion role
    """
    While True:
        table = Table(
            title="Menu Gestion",
            show_header=True,
            show_lines=True,
            show_edge=False,
            box=rich.box.SIMPLE,
            header_style="bold magenta",
        )
        table.add_column("Option", style="dim")
        table.add_column("Description", justify="left")
        
        table.add_row("1", "Gérer les collaborateurs")
        table.add_row("2", "Gérer les contrats")
        table.add_row("3", "Gérer les clients")
        table.add_row("4", "Gérer les événements")
        table.add_row("5", "Quitter")
        
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
            processing_task()
            break
        else:
            console.print("Choix invalide, veuillez réessayer", style="bold red")
