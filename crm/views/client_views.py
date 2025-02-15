import os
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import box
from datetime import datetime
from crm.controllers.client_controller import ClientController

console = Console()


def clear_screen():
    """
    Clear the screen
    """
    os.system("cls" if os.name == "nt" else "clear")


def display_client_list(clients):
    """
    Display a list of clients
    :param clients:
    :return: list of clients
    """
    clear_screen()
    table = Table(title="[bold blue]✨Liste des clients✨[/]", box=box.ROUNDED)
    table.add_column("[bold green]ID[/]", style="dim", width=6)
    table.add_column("[bold green]Nom complet[/]")
    table.add_column("[bold green]E-mail[/]")
    table.add_column("[bold green]Téléphone[/]")
    table.add_column("[bold green]Société[/]", style="blue")
    table.add_column("[bold green]Premier contact[/]")
    table.add_column("[bold green]Dernière mise à jour[/]")
    table.add_column("[bold green]Commercial[/]")
    for index, client in enumerate(clients, start=1):
        commercial_name = (
            client.commercial.full_name if client.commercial else "Non attribué"
        )
        table.add_row(
            str(index),
            # str(client.id),
            client.full_name,
            client.email,
            client.phone,
            client.company_name,
            client.first_contact_date.strftime("%d-%m-%Y"),
            client.last_update_date.strftime("%d-%m-%Y"),
            commercial_name,
        )

    console.print(Panel(table, title="🚀 Clients", expand=False))
    Prompt.ask("Appuyez sur une touche pour continuer...")


def create_client(db_session):
    """
    Display a form for creating a new client
    :return: dictionary with client data
    """
    clear_screen()
    console.print("[bold blue]➕ Création d'un nouveau client ➕[/]\n")

    full_name = Prompt.ask("[bold cyan]Nom complet du client[/]", default="John Doe")
    email = Prompt.ask("[bold cyan]E-mail du client[/]", default="adresse@email.com")
    phone = Prompt.ask("[bold cyan]Téléphone du client[/]", default="0102030405")
    company_name = Prompt.ask(
        "[bold cyan]Nom de la société du client[/]", default="Ma Société"
    )
    first_contact_date_str = Prompt.ask(
        "[bold cyan]Date du premier contact (DD-MM-YYYY)[/]",
        default=datetime.now().strftime("%d-%m-%Y"),
    )
    last_update_date_str = Prompt.ask(
        "[bold cyan]Date  mise à jour (DD-MM-YYYY)[/]",
        default=datetime.now().strftime("%d-%m-%Y"),
    )

    try:
        first_contact_date = datetime.strptime(
            first_contact_date_str, "%d-%m-%Y"
        ).date()
        last_update_date = datetime.strptime(last_update_date_str, "%d-%m-%Y").date()
    except ValueError:
        console.print("[bold red]❌ Les dates doivent être au format DD-MM-YYYY[/]")
        return None

    client_data = {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "company_name": company_name,
        "first_contact_date": first_contact_date,
        "last_update_date": last_update_date,
    }

    client_controller = ClientController(db_session)
    new_client = client_controller.create_client(client_data)
    if new_client:
        console.print("[bold green]✅ Nouveau client créé avec succès[/]")
        return new_client
    else:
        console.print(
            "[bold red]❌ Une erreur s'est produite lors de la création du client[/]"
        )
        return None


def select_client(clients):
    """
    Allow a user to select client from a list
    """
    clear_screen()
    display_client_list(clients)

    if not clients:
        console.print("[bold red]❌ Aucun client disponible pour créer un contrat[/]")
        return

    index = Prompt.ask("[bold cyan][1] Sélectionnez un client[/] | [0] Retour", default="1")
    if index == "0":
        console.clear()
        return
    try:
        index = int(index) - 1
        if 0 <= index < len(clients):
            return clients[index]
        else:
            console.print("[bold red]❌ L'ID sélectionné est invalide[/]")
            return None
    except ValueError:
        console.print("[bold red]❌ Entrée invalide[/]")
        return None


def update_client(db_session):
    """
    display a form for updating a client
    :param client:
    :return: updated client data
    """

    client_controller = ClientController(db_session)
    clients = client_controller.get_all_clients()
    if not clients:
        console.print("[bold red]❌ Aucun client disponible[/]")
        return

    client = select_client(clients)
    if not client:
        return

    clear_screen()
    console.print("[bold blue]🔄 Modification du client : {client.full_name}🔄[/]\n")

    full_name = Prompt.ask(
        "[bold cyan]Nom complet du client[/]", default=client.full_name
    )
    email = Prompt.ask("[bold cyan]E-mail du client[/]", default=client.email)
    phone = Prompt.ask("[bold cyan]Téléphone du client[/]", default=client.phone)
    company_name = Prompt.ask(
        "[bold cyan]Nom de la société du client[/]", default=client.company_name
    )
    first_contact_date_str = Prompt.ask(
        "[bold cyan]Date du premier contact (DD-MM-YYYY)[/]",
        default=client.first_contact_date.strftime("%d-%m-%Y"),
    )
    last_update_date = datetime.now().date()

    try:
        first_contact_date = datetime.strptime(
            first_contact_date_str, "%d-%m-%Y"
        ).date()
    except ValueError:
        console.print("[bold red]❌ Les dates doivent être au format DD-MM-YYYY[/]")
        return None

    updated_data = {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "company_name": company_name,
        "first_contact_date": first_contact_date,
        "last_update_date": last_update_date,
    }

    updated_client = client_controller.update_client(client.id, updated_data)
    if updated_client:
        console.print("[bold green]✅ Client mis à jour avec succès[/]")
        return updated_client
    else:
        console.print(
            "[bold red]❌ Une erreur s'est produite lors de la mise à jour du client[/]"
        )
        return None


def delete_client(db_session):
    """
    Ask confirmation before deleting a client
    :param db_session: database session
    :return: confirmation
    """
    client_controller = ClientController(db_session)
    clients = client_controller.get_all_clients()
    if not clients:
        console.print("[bold red]❌ Aucun client disponible pour créer un contrat[/]")
        return

    client = select_client(clients)
    if not client:
        return

    console.print(f"[bold red]⚠️ Suppression du client : {client.full_name}[/]")
    confirm = Confirm.ask("Confirmez-vous la suppression de ce client ?")
    if confirm:
        success = client_controller.delete_client(client.id)
        if success:
            console.print("[bold green]✅ Client supprimé avec succès[/]")
        else:
            console.print(
                "[bold red]❌ Une erreur s'est produite lors de la suppression du client[/]"
            )


def client_menu(db_session, create_mode=False, update_mode=False):
    """
    Display the client menu
    """
    client_controller = ClientController(db_session)

    if create_mode:
        create_client(db_session)
        return
    elif update_mode:
        update_client(db_session)
        return

    while True:
        clear_screen()

        console.print("[bold blue]👥 Menu Client 👥[/]")
        choice = Prompt.ask(
            "[bold cyan]1. Afficher clients | 2. Ajouter client | 3. Modifier client | 4. Supprimer "
            "client | 0. Retour[/]",
            choices=["1", "2", "3", "4", "0"],
        )

        if choice == "1":
            clients = client_controller.get_all_clients()
            display_client_list(clients)
        elif choice == "2":
            create_client(client_controller.db_session)
        elif choice == "3":
            update_client(client_controller.db_session)
        elif choice == "4":
            delete_client(client_controller.db_session)
        elif choice == "0":
            break
