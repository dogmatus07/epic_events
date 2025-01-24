from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box
from datetime import datetime

from ..controllers import contract_controller, user_controller
from ..views import user_views, contract_views

console = Console()


def display_events_list(events):
    """
    Display a list of events
    :param events:
    :return: list of events
    """
    table = Table(title="[bold blue]✨Liste des événements✨[/]", box=box.ROUNDED)
    table.add_column("[bold green]ID[/]", style="dim", width=12)
    table.add_column("[bold green]Contrat[/]")
    table.add_column("[bold green]Date de début[/]")
    table.add_column("[bold green]Date de fin[/]")
    table.add_column("[bold green]Lieu[/]")
    table.add_column("[bold green]Participants[/]")
    table.add_column("[bold green]Contact Support[/]")
    table.add_column("[bold green]Notes[/]")

    for event in events:
        contract_id = event.contract.id if event.contract else "Non attribué"
        support_name = event.support_contact.full_name if event.support_contact else "Non attribué"
        table.add_row(
            str(event.id),
            contract_id,
            event.event_date_start.strftime("%d-%m-%Y"),
            event.event_date_end.strftime("%d-%m-%Y"),
            event.location,
            str(event.attendees),
            support_name,
            event.notes
        )

    console.print(Panel(table, title="📆 Evénements", expand=False))


def create_event(db):
    """
    Display a form for creating a new event
    :param db:
    :return: event data
    """
    console.print("[bold blue]➕ Création d'un nouvel événement ➕[/]\n")

    # display the list of contracts
    contracts = contract_controller.get_contracts(db)
    contract_views.display_contract_list(contracts)

    # ask for the contract id
    contract_ids = [str(contract.id) for contract in contracts]
    if not contract_ids:
        console.print("[bold red]❌ Aucun contrat disponible pour créer un événement[/]")
        return None

    contract_id = Prompt.ask("[bold cyan]ID du contrat[/]", choices=contract_ids)

    # display the list of Support Users
    support_users = user_controller.get_support_users(db)
    user_views.display_user_list(support_users)

    # ask for the support user id
    support_ids = [str(user.id) for user in support_users]
    if not support_ids:
        console.print("[bold red]❌ Aucun utilisateur de support disponible pour créer un événement[/]")
        return None

    support_id = Prompt.ask("[bold cyan]ID de l'utilisateur de support[/]", choices=support_ids)
    event_date_start_str = Prompt.ask(
        "[bold cyan]Date de début de l'événement (DD-MM-YYYY)[/]",
        default=datetime.now().date()
    )
    event_date_end_str = Prompt.ask(
        "[bold cyan]Date de fin de l'événement (DD-MM-YYYY)[/]",
        default=datetime.now().date()
    )
    try:
        event_date_start_str = datetime.strptime(event_date_start_str, "%d-%m-%Y").date()
        event_date_end_str = datetime.strptime(event_date_end_str, "%d-%m-%Y").date()
    except ValueError:
        console.print("[bold red]❌ Les dates doivent être au format DD-MM-YYYY[/]")
        return None

    location = Prompt.ask("[bold cyan]Lieu de l'événement[/]", default="Paris")
    attendees = Prompt.ask("[bold cyan]Nombre de participants[/]", default=10)
    notes = Prompt.ask("[bold cyan]Notes[/]", default="")

    return {
        "contract_id": contract_id,
        "event_date_start": event_date_start_str,
        "event_date_end": event_date_end_str,
        "location": location,
        "attendees": attendees,
        "notes": notes,
        "support_id": support_id
    }


def update_event(event, db):
    """
    Display a form for updating an event
    :param event:
    :param db:
    :return: updated event data
    """
    console.print("[bold blue]🔄 Mise à jour de l'événement 🔄[/]\n")

    # display the list of contracts
    contracts = contract_controller.get_contracts(db)
    contract_views.display_contract_list(contracts)

    # ask for the contract id
    contract_ids = [str(contract.id) for contract in contracts]
    if not contract_ids:
        console.print("[bold red]❌ Aucun contrat disponible pour créer un événement[/]")
        return None

    contract_id = Prompt.ask("[bold cyan]ID du contrat[/]", choices=contract_ids, default=event.contract_id)

    # display the list of Support Users
    support_users = user_controller.get_support_users(db)
    user_views.display_user_list(support_users)

    # ask for the support user id
    support_ids = [str(user.id) for user in support_users]
    if not support_ids:
        console.print("[bold red]❌ Aucun utilisateur de support disponible pour créer un événement[/]")
        return None

    support_id = Prompt.ask(
        "[bold cyan]ID de l'utilisateur de support[/]",
        choices=support_ids, default=event.support_id
    )

    event_date_start_str = Prompt.ask(
        "[bold cyan]Date de début de l'événement (DD-MM-YYYY)[/]",
        default=event.event_date_start.strftime("%d-%m-%Y")
    )

    event_date_end_str = Prompt.ask(
        "[bold cyan]Date de fin de l'événement (DD-MM-YYYY)[/]",
        default=event.event_date_end.strftime("%d-%m-%Y")
    )
    try:
        event_date_start = datetime.strptime(event_date_start_str, "%d-%m-%Y").date()
        event_date_end = datetime.strptime(event_date_end_str, "%d-%m-%Y").date()
    except ValueError:
        console.print("[bold red]❌ Les dates doivent être au format DD-MM-YYYY[/]")
        return None

    location = Prompt.ask("[bold cyan]Lieu de l'événement[/]", default=event.location)
    attendees = Prompt.ask("[bold cyan]Nombre de participants[/]", default=event.attendees)
    notes = Prompt.ask("[bold cyan]Notes[/]", default=event.notes)

    return {
        "contract_id": contract_id,
        "event_date_start": event_date_start,
        "event_date_end": event_date_end,
        "location": location,
        "attendees": attendees,
        "notes": notes,
        "support_id": support_id
    }


def delete_event(event):
    """
    Display a form for deleting an event
    :param event:
    :return: boolean
    """
    console.print(f"[bold red]⚠️ Suppression de l'événement : {event.id} appartenant au contrat {event.contract}[/]")
    return Confirm.ask("[bold red]Confirmer la suppression ?[/]", default=False)

