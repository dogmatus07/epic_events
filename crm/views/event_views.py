from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box
from datetime import datetime

from sentry_sdk import capture_exception

from crm.controllers.event_controller import EventController
from crm.controllers.contract_controller import ContractController
from crm.controllers.user_controller import UserController
from crm.views.contract_views import select_contract
from crm.views.user_views import select_support_user
from crm.utils.console import clear_console

console = Console()


def display_events_list(events):
    """
    Display a list of events
    :param events:
    :return: list of events
    """
    if not events:
        console.print("[bold red]❌ Aucun événement disponible[/]")
        return
    table = Table(title="[bold blue]✨Liste des événements✨[/]", box=box.ROUNDED)
    table.add_column("[bold green]ID[/]", style="bold magenta", width=12)
    table.add_column("[bold green]Contrat[/]")
    table.add_column("[bold green]Date de début[/]")
    table.add_column("[bold green]Date de fin[/]")
    table.add_column("[bold green]Lieu[/]")
    table.add_column("[bold green]Participants[/]")
    table.add_column("[bold green]Contact Support[/]")
    table.add_column("[bold green]Notes[/]")

    for index, event in enumerate(events, start=1):
        contract_id = event.contract.id if event.contract else "Non attribué"
        support_contact = (
            event.support_contact.username if event.support_contact else "Non attribué"
        )
        table.add_row(
            str(index),
            contract_id,
            event.event_date_start.strftime("%d-%m-%Y"),
            event.event_date_end.strftime("%d-%m-%Y"),
            event.location,
            str(event.attendees),
            support_contact,
            event.notes,
        )

    console.print(Panel(table, title="📆 Evénements", expand=False))
    Prompt.ask("[bold cyan]Appuyez sur entrée pour continuer...[/]")


def select_event(events):
    """
    Display a list of events and ask the user to select one
    """
    if not events:
        console.print("[bold red]❌ Aucun événement disponible[/]")
        Prompt.ask("[bold cyan]Appuyez sur entrée pour continuer...[/]")
        return None

    display_events_list(events)
    choice = Prompt.ask(
        "[bold cyan]Que souhaitez-vous faire ? (1 : Sélectionner un événement | 0 : Retour)[/]",
        choices=["1", "0"],
    )
    if choice == "1":
        event_index = Prompt.ask(
            "[bold cyan]Sélectionnez un événement par son Index[/]",
            choices=[str(i) for i in range(1, len(events) + 1)],
        )
        return events[int(event_index) - 1]
    elif choice == "0":
        return None


def create_event(db_session):
    """
    Display a form for creating a new event
    :param db_session: database session
    :return: event data
    """
    console.print("[bold blue]➕ Création d'un nouvel événement ➕[/]\n")

    try:
        contracts = ContractController(db_session).get_all_contracts()
        selected_contract = select_contract(contracts)
        if not selected_contract:
            console.print(
                "[bold red]❌ Aucun contrat sélectionné pour créer un événement[/]"
            )
            return None
    except Exception as e:
        console.print(
            "[bold red]❌ Erreur lors de la récupération des contrats :[/]", e
        )
        return None

    support_users = UserController(db_session).get_all_support_users()
    if not support_users:
        console.print(
            "[bold red]❌ Aucun utilisateur de support disponible pour créer un événement[/]"
        )
        return None

    selected_support = select_support_user(support_users)
    if not selected_support:
        console.print(
            "[bold red]❌ Aucun utilisateur de support sélectionné pour créer un événement[/]"
        )
        return None

    event_date_start_str = Prompt.ask(
        "[bold cyan]Date de début de l'événement (DD-MM-YYYY)[/]",
        default=datetime.now().strftime("%d-%m-%Y"),
    )
    event_date_end_str = Prompt.ask(
        "[bold cyan]Date de fin de l'événement (DD-MM-YYYY)[/]",
        default=datetime.now().strftime("%d-%m-%Y"),
    )
    try:
        event_date_start_str = datetime.strptime(
            event_date_start_str, "%d-%m-%Y"
        ).date()
        event_date_end_str = datetime.strptime(event_date_end_str, "%d-%m-%Y").date()
    except ValueError as e:
        capture_exception(e)
        console.print("[bold red]❌ Les dates doivent être au format DD-MM-YYYY[/]")
        return None

    try:
        location = Prompt.ask("[bold cyan]Lieu de l'événement[/]", default="Paris")
        attendees = Prompt.ask("[bold cyan]Nombre de participants[/]", default=10)
        notes = Prompt.ask("[bold cyan]Notes[/]", default="")

        event_data = {
            "contract_id": selected_contract.id,
            "event_date_start": event_date_start_str,
            "event_date_end": event_date_end_str,
            "location": location,
            "attendees": int(attendees),
            "notes": notes,
            "support_id": selected_support.id,
        }
        return event_data
    except Exception as e:
        capture_exception(e)
        console.print("[bold red]❌ Erreur lors de la création de l'événement :[/]", e)
        return None


def update_event(event, db_session, is_support_user=False):
    """
    Display a form for updating an event
    :param event:
    :param db_session:
    :return: updated event data
    """
    console.print("[bold blue]🔄 Mise à jour de l'événement 🔄[/]\n")
    console.print(
        f"[bold cyan]Contrat lié à l'événement du client : {event.contract.client.full_name}[/]"
    )

    if not is_support_user:
        support_users = UserController(db_session).get_all_support_users()
        selected_support = select_support_user(support_users)
        support_id = selected_support.id if selected_support else event.support_id
    else:
        support_id = event.support_id

    event_date_start_str = Prompt.ask(
        "[bold cyan]Date de début de l'événement (DD-MM-YYYY)[/]",
        default=event.event_date_start.strftime("%d-%m-%Y"),
    )

    event_date_end_str = Prompt.ask(
        "[bold cyan]Date de fin de l'événement (DD-MM-YYYY)[/]",
        default=event.event_date_end.strftime("%d-%m-%Y"),
    )
    try:
        event_date_start = datetime.strptime(event_date_start_str, "%d-%m-%Y").date()
        event_date_end = datetime.strptime(event_date_end_str, "%d-%m-%Y").date()
    except ValueError as e:
        capture_exception(e)
        console.print("[bold red]❌ Les dates doivent être au format DD-MM-YYYY[/]")
        return None

    location = Prompt.ask("[bold cyan]Lieu de l'événement[/]", default=event.location)
    attendees = Prompt.ask(
        "[bold cyan]Nombre de participants[/]", default=event.attendees
    )
    notes = Prompt.ask("[bold cyan]Notes[/]", default=event.notes)

    return {
        "contract_id": event.contract_id,
        "event_date_start": event_date_start,
        "event_date_end": event_date_end,
        "location": location,
        "attendees": int(attendees),
        "notes": notes,
        "support_id": support_id,
    }


def delete_event(event, db_session):
    """
    Display a form for deleting an event
    :param event: event to delete
    :param db_session: database session
    :return: boolean
    """
    console.print(
        f"[bold red]⚠️ Suppression de l'événement : {event.id} appartenant au contrat {event.contract}[/]"
    )
    confirm = Confirm.ask("[bold red]Confirmer la suppression ?[/]", default=False)
    if confirm:
        try:
            controller = EventController(db_session)
            success = controller.delete_event(event.id)
            if success:
                console.print("[bold green]✅ Événement supprimé avec succès ![/]")
                return True
            else:
                console.print(
                    "[bold red]❌ Échec de la suppression de l'événement ![/]"
                )
        except Exception as e:
            capture_exception(e)
            console.print(
                "[bold red]❌ Erreur lors de la suppression de l'événement :[/]", e
            )

    return False


def event_menu(
    db_session,
    user_id,
    filter_mode=False,
    assign_support_mode=False,
    create_event_mode=False,
    update_event_mode=False,
    display_mode=False,
    support_only=False,
):
    """
    Menu to manage events
    :param db_session: database session
    :param filter_mode: filter events
    :param assign_support_mode: assign support user to event
    :param create_event_mode: create a new event
    :param update_event_mode: update an event
    :param support_only: display events assigned to support user
    :param display_mode: display all events
    :param user_id: user id
    """
    clear_console()
    event_controller = EventController(db_session, current_user_id=user_id)

    if filter_mode:
        events = event_controller.filter_events(support_only=support_only)
        display_events_list(events)
    elif assign_support_mode:
        events = event_controller.get_events(db_session)
        event = select_event(events)
        if event:
            support_users = UserController(db_session).get_all_support_users()
            selected_support = select_support_user(support_users)
            if selected_support:
                event_controller.assign_support(event.id, selected_support.id)
    elif display_mode:
        events = event_controller.get_events(db_session)
        display_events_list(events)
    elif create_event_mode:
        event_data = create_event(db_session)
        if event_data:
            event_controller.create_event(event_data)
    elif update_event_mode:
        current_user = EventController(
            db_session, current_user_id=user_id
        ).get_current_user()
        if not current_user:
            console.print("[bold red]❌ Utilisateur non trouvé[/]")
            Prompt.ask("[bold cyan]Appuyez sur entrée pour continuer...[/]")
            return
        is_support_user = current_user.role.role_name.strip().lower() == "support"
        events = event_controller.get_events(
            db_session, support_only=True if is_support_user else False
        )
        event = select_event(events)
        if event:
            updated_data = update_event(
                event, db_session, is_support_user=is_support_user
            )
            if updated_data:
                event_controller.update_event(event.id, updated_data)
