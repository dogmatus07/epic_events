import uuid
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import box
from ..controllers import client_controller
from ..views import client_views

console = Console()


def display_contract_list(contracts):
    """
    Display a list of contracts
    :param contracts:
    :return: list of contracts
    """
    table = Table(title="[bold blue]✨Liste des contrats✨[/]", box=box.ROUNDED)
    table.add_column("[bold green]ID[/]", style="dim", width=12)
    table.add_column("[bold green]Client[/]")
    table.add_column("[bold green]Montant total[/]")
    table.add_column("[bold green]Montant dû[/]")
    table.add_column("[bold green]Signé[/]")
    table.add_column("[bold green]Commercial[/]")
    for contract in contracts:
        client_name = contract.client.full_name if contract.client else "Non attribué"
        commercial_name = contract.commercial.full_name if contract.commercial else "Non attribué"
        signed_status = "✅ Yes" if contract.signed else "❌ No"
        table.add_row(
            str(contract.id),
            client_name,
            str(contract.total_amount),
            str(contract.amount_due),
            signed_status,
            commercial_name
        )
    console.print(Panel(table, title="📋 Contrats", expand=False))


def create_contract(db):
    """
    Display a form for creating a new contract
    :return: contract data
    """
    console.print("[bold blue]➕ Création d'un nouveau contrat ➕[/]\n")
    # display the list of clients
    clients = client_controller.get_clients(db)
    client_views.display_client_list(clients)

    # ask for the client id
    client_ids = [str(client.id) for client in clients]
    if not client_ids:
        console.print("[bold red]❌ Aucun client disponible pour créer un contrat[/]")
        return None

    client_id = Prompt.ask("[bold cyan]ID du client[/]", choices=client_ids)
    total_amount = Prompt.ask("[bold cyan]Montant total du contrat[/]", default=1000.0)
    amount_due = Prompt.ask("[bold cyan]Montant dû[/]", default=1000.0)
    signed = Confirm.ask("[bold cyan]Le contrat est-il signé ?[/]", default=False)

    return {
        'client_id': client_id,
        'total_amount': total_amount,
        'amount_due': amount_due,
        'signed': signed
    }


def update_contract(contract, db):
    """
    Display a form for updating a contract
    :param contract:
    :return: updated contract data
    """
    console.print("[bold blue]🔄 Mise à jour du contrat 🔄[/]\n")

    # display list of clients
    clients = client_controller.get_clients(db)
    client_views.display_client_list(clients)

    # ask for the client id
    client_ids = [str(client.id) for client in clients]
    if not client_ids:
        console.print("[bold red]❌ Aucun client disponible pour créer un contrat[/]")
        return None

    client_id = Prompt.ask("[bold cyan]ID du client[/]", choices=client_ids, default=contract.client_id)

    total_amount = Prompt.ask("[bold cyan]Montant total du contrat[/]", default=contract.total_amount)
    amount_due = Prompt.ask("[bold cyan]Montant dû[/]", default=contract.amount_due)
    signed = Confirm.ask("[bold cyan]Le contrat est-il signé ?[/]", default=contract.signed)

    return {
        "client_id": client_id,
        "total_amount": total_amount,
        "amount_due": amount_due,
        "signed": signed,
    }


def delete_contract(contract):
    """
    Display a form for deleting a contract
    :return: boolean
    """
    console.print(f"[bold red]⚠️ Suppression du contrat : {contract.id} appartenant au client {contract.client}[/]")
    return Confirm.ask("Confirmez-vous la suppression de ce contrat ?")