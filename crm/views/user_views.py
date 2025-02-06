import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt, Confirm

from crm.controllers.role_controller import RoleController
from crm.controllers.user_controller import UserController


console = Console()


def clear_screen():
    """
    Clear the screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')


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
        active_status = "✅ Oui" if user.is_active else "❌ Non"
        table.add_row(
            str(user.id),
            user.username,
            user.email,
            user.phone_number,
            user.role.role_name,
            active_status,
        )
    console.print(Panel(table, title="👩‍💼 Utilisateurs", expand=False))


def select_user(users, default_id=None):
    """
    Display a list of users and ask the user to select one
    """
    if not users:
        console.print("[bold red]❌ Aucun utilisateur disponible[/]")
        return None

    display_user_list(users)
    user_ids = [str(user.id) for user in users]
    selected_id = Prompt.ask(
        "[bold cyan]Sélectionnez un utilisateur par son ID[/]",
        default=default_id if default_id in user_ids else None,
        choices=user_ids
    )
    return next((user for user in users if str(user.id) == selected_id), None)


def create_user(db_session):
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

    # get the list of roles
    roles = RoleController(db_session).get_all_roles()
    if not roles:
        console.print("[bold red]❌ Aucun rôle disponible pour créer un utilisateur[/]")
        return None

    console.print("[bold blue]Liste des rôles disponibles[/]")
    for role in roles:
        console.print(f"[bold green]{role.role_name}[/]")

    role_name = Prompt.ask(
        "[bold cyan]Rôle de l'utilisateur[/]", choices=[role.role_name for role in roles]
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


def update_user(user, db_session):
    """
    Display a form for updating a user
    :param user:
    :param db_session:
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
    # get available roles
    roles = RoleController(db_session).get_all_roles()
    if not roles:
        console.print("[bold red]❌ Aucun rôle disponible pour créer un utilisateur[/]")
        return None
    else:
        console.print("[bold blue]Liste des rôles disponibles[/]")
        for role in roles:
            console.print(f"[bold green]{role.role_name}[/]")
        role_name = Prompt.ask(
            "[bold cyan]Rôle de l'utilisateur[/]",
            choices=[role.role_name for role in roles],
            default=user.role.role_name
        )

    password = Prompt.ask(
        "[bold cyan]Mot de passe[/] (laissez vide pour ne pas le changer)",
        password=True, default=""
    )

    user_data = {
        "username": username,
        "email": email,
        "phone_number": phone_number,
        "is_active": is_active,
        "role_name": role_name,
        "password": password
    }
    return user_data


def delete_user(user):
    """
    Display a form for deleting a user
    :param user:
    :return: None
    """
    console.print(f"[bold red]⚠️ Suppression de l'utilisateur : {user.full_name} - {user.username} - {user.email}[/]")
    return Confirm.ask("[bold red]⚠️ Voulez-vous vraiment supprimer cet utilisateur ?[/]", default=False)


def user_menu(db_session):
    """
    Display the user menu
    :param db_session: database session
    """

    user_controller = UserController(db_session)
    clear_screen()
    while True:
        console.print("[bold blue]👩‍💼 Menu Utilisateur 👩‍💼[/]")
        choice = Prompt.ask(
            "[bold cyan]1. Afficher utilisateurs | 2. Ajouter utilisateur | 3. Modifier utilisateur | 4. Supprimer "
            "utilisateur | 0. Retour[/]",
            choices = ["1", "2", "3", "4", "0"]
        )

        if choice == "1":
            users = user_controller.get_all_users()
            display_user_list(users)
        elif choice == "2":
            user_data = create_user(db_session)
            if user_data:
                user_controller.create_user(user_data)
        elif choice == "3":
            users = user_controller.get_all_users()
            if users:
                user = select_user(users)
                if user:
                    updated_user_data = update_user(user, db_session)
                    if updated_user_data:
                        user_controller.update_user(user.id, updated_user_data)
        elif choice == "4":
            users = user_controller.get_all_users()
            if users:
                user = select_user(users)
                if user:
                    confirm = delete_user(user)
                    if confirm:
                        user_controller.delete_user(user.id)
        elif choice == "0":
            break


def select_support_user(support_users):
    """
    Display a list of support users and ask the user to select one
    :param support_users: list of support users
    """
    if not support_users:
        console.print("[bold red]❌ Aucun utilisateur de support disponible[/]")
        return None

    console.print("[bold blue]‍💼 Liste des utilisateurs de support[/]")
    for index, user in enumerate(support_users, start=1):
        console.print(f"[bold green]{index}. {user.full_name} - {user.email}[/]")

    user_index = Prompt.ask(
        "[bold cyan]Sélectionnez un utilisateur de support par son index[/]",
        choices=[str(i) for i in range(1, len(support_users) + 1)]
    )
    return support_users[int(user_index) - 1]