import pytest
import uuid
from crm.views.contract_views import (
    create_contract,
    update_contract,
    delete_contract,
    select_contract,
    filter_contract_menu,
)
from crm.controllers import ContractController
from crm.models.models import Contract


def test_create_contract_view(db_session, test_client, monkeypatch):
    """
    Test create_contract view
    """
    inputs = iter(
        [
            test_client.id,
            "1000",  # total_amount
            "500",  # amount_due
            "y",
            "",
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda *args: next(inputs),
    )
    monkeypatch.setattr(
        "rich.prompt.Prompt.ask",
        lambda *args, **kwargs: "1",
    )

    contract = create_contract(db_session)
    assert contract is not None
    assert contract.total_amount == 1.0


def test_update_contract_view(db_session, test_client, monkeypatch):
    """
    Test update_contract view
    """

    db_session.query(Contract).delete()
    db_session.commit()

    # create a fake contract
    controller = ContractController(db_session)
    contract_data = {
        "client_id": test_client.id,
        "total_amount": 1000,
        "amount_due": 500,
        "signed": True,
    }

    controller.create_contract(contract_data)

    prompt_value = iter(
        [
            "",  # enter key to continue
            "1",  # select contract menu
            "1",  # select contract index
            "1000",  # total_amount
            "500",  # amount_due
            "y",
            "",
        ]
    )

    monkeypatch.setattr(
        "rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_value)
    )
    monkeypatch.setattr("rich.prompt.Confirm.ask", lambda *args, **kwargs: True)
    updated_contract = update_contract(db_session)
    assert updated_contract is not None
    assert updated_contract.total_amount == 1000.0


def test_delete_contract_view(db_session, test_client, monkeypatch):
    """
    Test delete_contract view
    """
    db_session.query(Contract).delete()
    db_session.commit()

    # create a fake contract
    controller = ContractController(db_session)
    contract_data = {
        "client_id": test_client.id,
        "total_amount": 1000,
        "amount_due": 500,
        "signed": True,
    }

    contract = controller.create_contract(contract_data)

    prompt_value = iter(
        [
            "",  # enter key to continue
            "1",  # select contract menu
            "1",  # select contract index
            "y",  # confirm deletion
            "",
        ]
    )

    monkeypatch.setattr(
        "rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_value)
    )
    monkeypatch.setattr("rich.prompt.Confirm.ask", lambda *args, **kwargs: True)

    delete_contract(db_session)

    remaining_contract = controller.get_all_contracts()
    assert len(remaining_contract) == 0


def test_select_contract_view(monkeypatch, db_session):
    """
    Test the select_contract function to ensure it returns a contract object based on user input.
    """

    controller = ContractController(db_session)

    # create a fake contract
    contract_data_1 = {
        "client_id": str(uuid.uuid4()),
        "total_amount": 1000,
        "amount_due": 500,
        "signed": True,
    }
    contract_data_2 = {
        "client_id": str(uuid.uuid4()),
        "total_amount": 2000,
        "amount_due": 1000,
        "signed": False,
    }

    contract_client_1 = controller.create_contract(contract_data_1)
    contract_client_2 = controller.create_contract(contract_data_2)
    contracts = controller.get_all_contracts()
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: "1")
    selected_contract = select_contract(contracts)
    assert len(contracts) == 2
    assert selected_contract is not None
    assert selected_contract.id == contract_client_1.id


def test_filter_contract_menu(monkeypatch, db_session):
    """
    Test the filter_contract function to ensure it returns a list of contracts based on user input.
    """
    controller = ContractController(db_session)

    # create a fake contract
    contract_data_1 = {
        "client_id": str(uuid.uuid4()),
        "total_amount": 1000,
        "amount_due": 500,
        "signed": True,
    }
    contract_data_2 = {
        "client_id": str(uuid.uuid4()),
        "total_amount": 2000,
        "amount_due": 1000,
        "signed": False,
    }

    controller.create_contract(contract_data_1)
    controller.create_contract(contract_data_2)

    prompt_sequence = iter(
        ["2", "3", "4", "5", "0"]
    )  # Simulate user input for filtering
    monkeypatch.setattr(
        "rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_sequence)
    )
    monkeypatch.setattr(
        "crm.views.contract_views.display_menu",
        lambda title, options: next(prompt_sequence),
    )
    monkeypatch.setattr(
        "crm.views.contract_views.display_contract_list", lambda contracts: None
    )

    filter_contract_menu(db_session)
    assert True
