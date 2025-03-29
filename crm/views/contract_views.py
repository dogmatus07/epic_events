from rich.console import Console
from crm.views.views import clear_console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import box
from sentry_sdk import capture_exception

from crm.controllers.contract_controller import ContractController
from crm.controllers.client_controller import ClientController
from crm.views.client_views import select_client
from crm.views.views import display_menu
from crm.utils.console import clear_console

console = Console()


def display_contract_list(contracts):
    """
    Display a list of contracts
    :param contracts:
    :return: list of contracts
    """
    clear_console()
    table = Table(title="[bold blue]✨Liste des contrats✨[/]", box=box.ROUNDED)
    table.add_column("[bold green]Index[/]", style="bold magenta", width=6)
    options = [
        "ID Contrat",
        "Client",
        "Montant total",
        "Montant dû",
        "Signé",
        "Commercial",
    ]
    for idx, option in enumerate(options, start=1):
        table.add_column(f"[bold green]{option}[/]")
    for idx, contract in enumerate(contracts, start=1):
        client_name = contract.client.full_name if contract.client else "Non attribué"
        table.add_row(
            str(idx),
            str(contract.id),
            client_name,
            f"{contract.total_amount}",
            f"{contract.amount_due}",
            "✅" if contract.signed else "❌",
            contract.commercial.username if contract.commercial else "Non attribué",
        )

    console.print(Panel(table, title="📋 Contrats", expand=False))
    Prompt.ask("[bold cyan]Appuyez sur entrée pour continuer[/]")


def select_contract(contracts):
    """
    Display a list of contracts and ask the user to select one
    """
    if not contracts:
        console.print("[bold red]❌ Aucun contrat disponible[/]")
        return None

    display_contract_list(contracts)
    choice = Prompt.ask(
        "[bold cyan]Que souhaitez-vous faire ? (1: Choisir un contrat à modifier | 0: Retour[/]",
        choices=["1", "0"],
    )
    if choice == "0":
        return None
    elif choice == "1":
        try:
            index = Prompt.ask(
                "[bold cyan]Sélectionnez un contrat par son index[/]", default=1
            )
            if 1 <= int(index) <= len(contracts):
                return contracts[int(index) - 1]
            else:
                console.print("[bold red]❌ Index invalide[/]")
                return None
        except ValueError as e:
            capture_exception(e)
            console.print("[bold red]❌ Entrée invalide[/]")
            return None


def create_contract(db_session):
    """
    Display a form for creating a new contract
    :return: contract data
    """
    console.print("[bold blue]➕ Création d'un nouveau contrat ➕[/]\n")
    # display the list of clients
    try:
        client_controller = ClientController(db_session)
        clients = client_controller.get_all_clients()

        if not clients:
            console.print(
                "[bold red]❌ Aucun client disponible pour créer un contrat[/]"
            )
            return None
    except Exception as e:
        capture_exception(e)
        console.print(
            "[bold red]❌ Une erreur s'est produite lors de la récupération des clients[/]"
        )
        return None

    # select a client
    client = select_client(clients)
    if not client:
        return None

    try:
        total_amount = float(
            Prompt.ask("[bold cyan]Montant total du contrat[/]", default="1000")
        )
        amount_due = float(Prompt.ask("[bold cyan]Montant dû[/]", default="1000"))
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
    except Exception as e:
        capture_exception(e)
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
    try:
        contact_controller = ContractController(db_session)
        contracts = contact_controller.get_all_contracts()

        if not contracts:
            console.print(
                "[bold red]❌ Aucun contrat disponible pour créer un contrat[/]"
            )
            return None
    except Exception as e:
        capture_exception(e)
        console.print(
            "[bold red]❌ Une erreur s'est produite lors de la récupération des contrats[/]"
        )
        return None

    # Select a contract to update
    contract = select_contract(contracts)
    if not contract:
        return None

    try:
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
    except Exception as e:
        capture_exception(e)
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

    try:
        contract_controller = ContractController(db_session)
        contracts = contract_controller.get_all_contracts()

        if not contracts:
            console.print(
                "[bold red]❌ Aucun contrat disponible pour supprimer un contrat[/]"
            )
            return
    except Exception as e:
        capture_exception(e)
        console.print(
            "[bold red]❌ Une erreur s'est produite lors de la récupération des contrats[/]"
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
        try:
            success = contract_controller.delete_contract(contract.id)
            if success:
                console.print("[bold green]✅ Contrat supprimé avec succès[/]")
            else:
                console.print(
                    "[bold red]❌ Une erreur s'est produite lors de la suppression du contrat[/]"
                )
        except Exception as e:
            capture_exception(e)
            console.print(
                "[bold red]❌ Erreur inattendue lors de la suppression du contrat[/]"
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
        Prompt.ask("[bold cyan]Appuyez sur entrée pour continuer[/]")
        return
    clear_console()

    while True:
        table = Table(title="[bold blue]📝 Menu Contrat 📝[/]", box=box.ROUNDED)
        table.add_column("[bold green]Index[/]", style="bold magenta", width=6)
        table.add_column("[bold green]Options[/]")
        options = [
            "Afficher contrats",
            "Ajouter contrat",
            "Modifier contrat",
            "Supprimer contrat",
            "Retour",
        ]
        for idx, option in enumerate(options, start=1):
            table.add_row(str(idx), option)
        console.print(Panel(table, title="🔧 EPIC EVENTS CRM", expand=False))
        choice = Prompt.ask(
            "[bold cyan]Choisissez une option[/]",
            choices=["1", "2", "3", "4", "5"],
        )

        if choice == "1":
            contracts = contract_controller.get_all_contracts()
            display_contract_list(contracts)
            Prompt.ask("[bold cyan]Appuyez sur entrée pour retourner au menu[/]")
            clear_console()
        elif choice == "2":
            create_contract(db_session)
        elif choice == "3":
            update_contract(db_session)
        elif choice == "4":
            delete_contract(db_session)
        elif choice == "5":
            break


def filter_contract_menu(db_session):
    """
    Display the contract menu
    :param db_session: database session
    """
    clear_console()
    contract_controller = ContractController(db_session)

    options = {
        "1": "Afficher tous les contrats",
        "2": "Afficher les contrats non signés",
        "3": "Afficher les contrats non payé totalement",
        "4": "Afficher les contrats signés",
        "5": "Afficher les contrats payés totalement",
        "0": "Retour",
    }
    contracts = []
    while True:
        choice = display_menu("Filtrer les contrats", options)
        if choice == "0":
            break
        elif choice == "1":
            contracts = contract_controller.get_all_contracts()
        elif choice == "2":
            contracts = contract_controller.filter_contract(signed=False)
        elif choice == "3":
            contracts = contract_controller.filter_contract(fully_paid=False)
        elif choice == "4":
            contracts = contract_controller.filter_contract(signed=True)
        elif choice == "5":
            contracts = contract_controller.filter_contract(fully_paid=True)
        display_contract_list(contracts)
