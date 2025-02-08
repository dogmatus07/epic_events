import os
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich import box

from crm.views.client_views import client_menu
from crm.views.contract_views import contract_menu
from crm.views.event_views import event_menu
from crm.views.user_views import user_menu

console = Console()


def clear_screen():
    """
    Clear the screen
    """
    os.system("cls" if os.name == "nt" else "clear")


def display_menu(title, options):
    """
    Display menu with common styling
    :param title: menu title
    :param options: list of options
    """
    clear_screen()

    table = Table(title=f"[bold blue]✨{title}✨[/]", box=box.ROUNDED)
    table.add_column("[bold green]Index[/]", style="dim", width=6)
    table.add_column("[bold green]Description[/]")

    for keys, values in options.items():
        table.add_row(keys, values)

    console.print(Panel(table, title="🔧 EPIC EVENTS CRM", expand=False))

    return Prompt.ask("[bold cyan]Choisissez une option[/]", choices=options.keys())


def gestion_menu(db_session, user_id):
    """
    Display the specific menu for role : Gestion
    """
    while True:
        choice = display_menu(
            "Menu Gestion",
            {
                "1": "Gérer Collaborateurs",
                "2": "Gérer Contrats",
                "3": "Afficher Événements",
                "4": "Assigner Support",
                "0": "Quitter",
            },
        )

        if choice == "1":
            user_menu(db_session)
        elif choice == "2":
            contract_menu(db_session)
        elif choice == "3":
            event_menu(db_session, user_id, display_mode=True)
        elif choice == "4":
            event_menu(db_session, user_id, assign_support_mode=True)
        elif choice == "0":
            break


def commercial_menu(db_session, user_id):
    """
    Display the specific menu for role : Commercial
    """
    while True:
        choice = display_menu(
            "Menu Commercial",
            {
                "1": "Créer Clients",
                "2": "Mettre à jour Clients",
                "3": "Modifier Contrats",
                "4": "Créer Événement",
                "5": "Filtrer Contrats",
                "0": "Quitter",
            },
        )

        if choice == "1":
            client_menu(db_session, create_mode=True)
        elif choice == "2":
            client_menu(db_session, update_mode=True)
        elif choice == "3":
            contract_menu(db_session, update_mode=True)
        elif choice == "4":
            event_menu(db_session, user_id, create_event_mode=True)
        elif choice == "5":
            contract_menu(db_session, filter_mode=True)
        elif choice == "0":
            break


def support_menu(db_session, user_id):
    """
    Display the specific menu for role : Support
    :param db_session: database session
    :param user_id: user id
    """
    while True:
        choice = display_menu(
            "Menu Support",
            {
                "1": "Afficher Événements",
                "2": "Mettre à jour Événements",
                "0": "Quitter",
            },
        )

        if choice == "1":
            event_menu(db_session, user_id, filter_mode=True, support_only=True)
        elif choice == "2":
            event_menu(db_session, user_id, update_event_mode=True, support_only=True)
        elif choice == "0":
            break


def main_menu(role, db_session, user_id):
    """
    Display the main menu based on the user's role
    :param role: user's role
    :param db_session: database session
    """
    role_menus = {
        "Gestion": lambda: gestion_menu(db_session, user_id),
        "Commercial": lambda: commercial_menu(db_session, user_id),
        "Support": lambda: support_menu(db_session, user_id),
    }

    menu_function = role_menus.get(role)
    if menu_function:
        menu_function()
    else:
        console.print("[bold red]❌ Rôle non reconnu[/]")
        return None
