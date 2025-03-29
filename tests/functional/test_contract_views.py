import pytest
from crm.views.contract_views import create_contract, update_contract, delete_contract
from crm.controllers import ContractController
from crm.models.models import Contract


def test_create_contract_view(db_session, test_client, monkeypatch):
    """
    Test create_contract view
    """
    inputs = iter(
        [
            test_client.id,
            "1000", # total_amount
            "500", # amount_due
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
            "", # enter key to continue
            "1", # select contract menu
            "1", # select contract index
            "1000", # total_amount
            "500", # amount_due
            "y",
            "",
        ]
    )

    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_value))
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
            "", # enter key to continue
            "1", # select contract menu
            "1", # select contract index
            "y", # confirm deletion
            "",
        ]
    )

    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(prompt_value))
    monkeypatch.setattr("rich.prompt.Confirm.ask", lambda *args, **kwargs: True)

    delete_contract(db_session)

    remaining_contract = controller.get_all_contracts()
    assert len(remaining_contract) == 0