import os
import uuid
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import box
from crm.controllers.contract_controller import ContractController
from crm.controllers.client_controller import ClientController
from crm.views.client_views import select_client

console = Console()


def clear_screen():
    """
    Clear the screen
    """
    os.system("cls" if os.name == "nt" else "clear")


def display_contract_list(contracts):
    """
    Display a list of contracts
    :param contracts:
    :return: list of contracts
    """
    console.clear()
    table = Table(title="[bold blue]✨Liste des contrats✨[/]", box=box.ROUNDED)
    table.add_column("[bold green]Index[/]", style="dim", width=6)
    options = ["ID Contrat", "Client", "Montant total", "Montant dû", "Signé", "Commercial"]
    for idx, option in enumerate(options, start=1):
        table.add_column(f"[bold green]{option}[/]")
    for idx, contract in enumerate(contracts, start=1):
        client_name = contract.client.full_name if contract.client else "Non attribué"
        table.add_row(
            str(idx),
            str(contract.id),
            client_name,
            str(contract.total_amount),
            str(contract.amount_due),
            "✅" if contract.signed else "❌",
            contract.commercial.full_name if contract.commercial else "Non attribué",
        )

    console.print(Panel(table, title="📋 Contrats", expand=False))


def select_contract(contracts):
    """
    Display a list of contracts and ask the user to select one
    """
    if not contracts:
        console.print("[bold red]❌ Aucun contrat disponible[/]")
        return None

    display_contract_list(contracts)
    try:
        index = Prompt.ask("[bold cyan]Sélectionnez un contrat[/]", default=1)
        if 1 <= int(index) <= len(contracts):
            return contracts[int(index) - 1]
        else:
            console.print("[bold red]❌ Index invalide[/]")
            return None
    except ValueError:
        console.print("[bold red]❌ Entrée invalide[/]")
        return None


def create_contract(db_session):
    """
    Display a form for creating a new contract
    :return: contract data
    """
    console.print("[bold blue]➕ Création d'un nouveau contrat ➕[/]\n")
    # display the list of clients
    client_controller = ClientController(db_session)
    clients = client_controller.get_all_clients()
    console.clear()

    if not clients:
        console.print("[bold red]❌ Aucun client disponible pour créer un contrat[/]")
        return None

    # select a client
    client = select_client(clients)
    if not client:
        return None

    total_amount = Prompt.ask("[bold cyan]Montant total du contrat[/]", default=1000.0)
    amount_due = Prompt.ask("[bold cyan]Montant dû[/]", default=1000.0)
    signed = Confirm.ask("[bold cyan]Le contrat est-il signé ?[/]", default=False)

    contract_data = {
        "client_id": client.id,
        "total_amount": total_amount,
        "amount_due": amount_due,
        "signed": signed,
    }

    contract_controller = ContractController(db_session)
    created_contract = contract_controller.create_contract(contract_data)

    if created_contract:
        console.print("[bold green]✅ Nouveau contrat créé avec succès[/]")
        return created_contract
    else:
        console.print(
            "[bold red]❌ Une erreur s'est produite lors de la création du contrat[/]"
        )
        return None


def update_contract(db_session):
    """
    Display a form for updating a contract
    :param contract:
    :return: updated contract data
    """
    console.print("[bold blue]🔄 Mise à jour du contrat 🔄[/]\n")
    contact_controller = ContractController(db_session)
    contracts = contact_controller.get_all_contracts()

    if not contracts:
        console.print("[bold red]❌ Aucun contrat disponible pour créer un contrat[/]")
        return None

    # Select a contract to update
    contract = select_contract(contracts)
    if not contract:
        return None

    total_amount = Prompt.ask(
        "[bold cyan]Montant total du contrat[/]", default=contract.total_amount
    )
    amount_due = Prompt.ask("[bold cyan]Montant dû[/]", default=contract.amount_due)
    signed = Confirm.ask(
        "[bold cyan]Le contrat est-il signé ?[/]", default=contract.signed
    )

    updated_data = {
        "total_amount": total_amount,
        "amount_due": amount_due,
        "signed": signed,
    }

    updated_contract = contact_controller.update_contract(contract.id, updated_data)
    if updated_contract:
        console.print("[bold green]✅ Contrat mis à jour avec succès[/]")
        return updated_contract
    else:
        console.print(
            "[bold red]❌ Une erreur s'est produite lors de la mise à jour du contrat[/]"
        )
        return None


def delete_contract(db_session):
    """
    Display a form for deleting a contract
    :return: boolean
    """
    console.print("[bold blue]⚠️ Suppression d'un contrat [/]\n")
    contract_controller = ContractController(db_session)
    contracts = contract_controller.get_all_contracts()

    if not contracts:
        console.print(
            "[bold red]❌ Aucun contrat disponible pour supprimer un contrat[/]"
        )
        return

    # select a contract to delete
    contract = select_contract(contracts)
    if not contract:
        return

    confirm = Confirm.ask(
        f"[bold red]⚠️ Voulez-vous vraiment supprimer le contrat appartenant à : {contract.client.full_name}?[/]",
        default=False,
    )
    if confirm:
        success = contract_controller.delete_contract(contract.id)
        if success:
            console.print("[bold green]✅ Contrat supprimé avec succès[/]")
        else:
            console.print(
                "[bold red]❌ Une erreur s'est produite lors de la suppression du contrat[/]"
            )


def contract_menu(db_session, update_mode=False, filter_mode=False):
    """
    Display the contract menu
    :param db_session: database session
    :param update_mode: boolean
    :param filter_mode: boolean
    """
    contract_controller = ContractController(db_session)

    if update_mode:
        update_contract(db_session)
        return
    elif filter_mode:
        contracts = contract_controller.get_all_contracts()
        display_contract_list(contracts)
        return
    console.clear()

    while True:
        table = Table(title="[bold blue]📝 Menu Contrat 📝[/]", box=box.ROUNDED)
        table.add_column("[bold green]Index[/]", style="dim", width=6)
        table.add_column("[bold green]Options[/]")
        options = ["Afficher contrats", "Ajouter contrat", "Modifier contrat", "Supprimer contrat", "Retour"]
        for idx, option in enumerate(options, start=1):
            table.add_row(str(idx), option)
        console.print(Panel(table, title="🔧 EPIC EVENTS CRM", expand=False))
        choice = Prompt.ask(
            "[bold cyan]Choisissez une option[/]",
            choices=["1", "2", "3", "4", "0"],
        )

        if choice == "1":
            contracts = contract_controller.get_all_contracts()
            display_contract_list(contracts)
            Prompt.ask("[bold cyan]Appuyez sur une touche pour retourner au menu[/]")
        elif choice == "2":
            create_contract(db_session)
        elif choice == "3":
            update_contract(db_session)
        elif choice == "4":
            delete_contract(db_session)
        elif choice == "0":
            break
