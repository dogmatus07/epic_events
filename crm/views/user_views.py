from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt, Confirm
from datetime import datetime

from ..controllers import contract_controller, user_controller
from ..views import user_views, contract_views

console = Console()


def display_user_list(users):
    """
    Display a list of users
    :param users:
    :return: list of users
    """
    table = Table(title="[bold blue]✨Liste des utilisateurs✨[/]", box=box.ROUNDED)
    table.add_column("[bold green]ID[/]", style="dim", width=12)
    table.add_column("[bold green]Nom complet[/]")
    table.add_column("[bold green]E-mail[/]")
    table.add_column("[bold green]Téléphone[/]")
    table.add_column("[bold green]Rôle[/]")
    table.add_column("[bold green]Actif[/]")
    table.add_column("[bold green]Date de création[/]")

    for user in users:
        active_status = "✅ Yes" if user.is_active else "❌ No"
        table.add_row(
            str(user.id),
            user.full_name,
            user.email,
            user.phone_number,
            user.role.role_name,
            active_status,
            user.date_created
        )
    console.print(Panel(table, title="👩‍💼 Utilisateurs", expand=False))


def create_user():
    """
    Display a form for creating a new user
    :return: dictionary with user data
    """
    console.print("[bold blue]➕ Création d'un nouvel utilisateur ➕[/]\n")
    username = Prompt.ask(
        "[bold cyan]Nom d'utilisateur[/]",
        default="john_doe"
    )
    email = Prompt.ask(
        "[bold cyan]E-mail de l'utilisateur[/]",
        default="adresse@email.com"
    )
    phone_number = Prompt.ask(
        "[bold cyan]Téléphone[/]",
        default="0102030405"
    )
    is_active = Confirm.ask(
        "[bold cyan]Activer l'utilisateur ?[/]",
        default=True
    )
    role_name = Prompt.ask(
        "[bold cyan]Rôle de l'utilisateur[/]",
        default="Gestion"
    )
    password = Prompt.ask(
        "[bold cyan]Mot de passe[/]",
        password=True
    )

    return {
        "username": username,
        "email": email,
        "phone_number": phone_number,
        "is_active": is_active,
        "role_name": role_name,
        "password": password
    }


def update_user(user):
    """
    Display a form for updating a user
    :param user:
    :return: updated user data
    """
    console.print(f"[bold blue]🔄 Modification de l'utilisateur : {user.full_name}🔄[/]\n")

    username = Prompt.ask(
        "[bold cyan]Nom d'utilisateur[/]",
        default=user.username
    )
    email = Prompt.ask(
        "[bold cyan]E-mail de l'utilisateur[/]",
        default=user.email
    )
    phone_number = Prompt.ask(
        "[bold cyan]Téléphone[/]",
        default=user.phone_number
    )
    is_active = Confirm.ask(
        "[bold cyan]Activer l'utilisateur ?[/]",
        default=user.is_active
    )
    role_name = Prompt.ask(
        "[bold cyan]Rôle de l'utilisateur[/]",
        default=user.role.role_name
    )
    password = Prompt.ask(
        "[bold cyan]Mot de passe[/]",
        password=True
    )

    return {
        "username": username,
        "email": email,
        "phone_number": phone_number,
        "is_active": is_active,
        "role_name": role_name,
        "password": password
    }


def delete_user(user):
    """
    Display a form for deleting a user
    :param user:
    :return: None
    """
    console.print(f"[bold red]⚠️ Suppression de l'utilisateur : {user.full_name}[/]")
    return Confirm.ask("")
