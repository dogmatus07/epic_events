from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich import box

from crm.views.client_views import client_menu
from crm.views.contract_views import contract_menu
from crm.views.event_views import event_menu
from crm.views.user_views import user_menu

console = Console()


def gestion_menu():
    """
    Display the specific menu for role : Gestion
    """
    while True:
        table = Table(title="[bold blue]✨Menu Gestion✨[/]", box=box.ROUNDED)
        table.add_column("[bold green]1. Collaborateurs[/]", style="dim", width=12)
        table.add_column("[bold green]2. Contrats[/]")
        table.add_column("[bold green]3. Evénements[/]")
        table.add_column("[bold green]4. Assigner[/]")
        table.add_column("[bold green]0. Retour[/]")

        console.print(Panel(table, title="🔧 Menu Gestion", expand=False))
        choice = Prompt.ask("[bold cyan]Choisissez une option[/]", choices=["1", "2", "3", "4", "5"])

        if choice == "1":
            user_menu()
        elif choice == "2":
            contract_menu()
        elif choice == "3":
            event_menu(filter_mode=True)
        elif choice == "4":
            event_menu(assign_support_mode=True)
        elif choice == "0":
            break


def commercial_menu():
    """
    Display the specific menu for role : Commercial
    """
    while True:
        table = Table(title="[bold blue]✨Menu Commercial✨[/]", box=box.ROUNDED)
        table.add_column("[bold green]1. Créer Clients[/]", style="dim", width=12)
        table.add_column("[bold green]2. Mettre à jour Clients[/]")
        table.add_column("[bold green]3. Modifier Contrats[/]")
        table.add_column("[bold green]4. Créer Événement[/]")
        table.add_column("[bold green]5. Filtrer Contrats[/]")
        table.add_column("[bold green]6. Retour[/]")

        console.print(Panel(table, title="🔧 Bienvenue", expand=False))
        choice = Prompt.ask("[bold cyan]Choisissez une option[/]", choices=["1", "2", "3", "4", "5", "0"])

        if choice == "1":
            client_menu(create_mode=True)
        elif choice == "2":
            client_menu(update_mode=True)
        elif choice == "3":
            contract_menu(update_mode=True)
        elif choice == "4":
            event_menu(create_mode=True)
        elif choice == "5":
            contract_menu(filter_mode=True)
        elif choice =="0":
            break


def support_menu():
    """
    Display the specific menu for role : Support
    """
    while True:
        table = Table(title="[bold blue]✨ Menu Support ✨[/]", box=box.ROUNDED)
        table.add_column("[bold green]Index[/]", style="dim", width=12)
        table.add_column("[bold green]Description[/]")

        # adding rows
        table.add_row("1", "Afficher les événements")
        table.add_row("2", "Mettre à jour les événements")
        table.add_row("0", "Retour")

        console.print(Panel(table, title="🔧 EPIC EVENTS CRM", expand=False))
        choice = Prompt.ask("[bold cyan]Choisissez une option[/]", choices=["1", "2", "0"])

        if choice == "1":
            event_menu(filter_mode=True, support_only=True)
        elif choice == "2":
            event_menu(update_event_mode=True, support_only=True)
        elif choice == "0":
            break


def main_menu(role):
    """
    Display the main menu based on the user's role
    :param role: user's role
    """
    if role == "Gestion":
        gestion_menu()
    elif role == "Commercial":
        commercial_menu()
    elif role == "Support":
        support_menu()
    else:
        console.print("[bold red]❌ Rôle inconnu - Contactez l'administrateur[/]")
        return

