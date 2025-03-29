import pytest
from crm.controllers.contract_controller import ContractController
from crm.models.models import Contract
import uuid


def test_create_contract(db_session):
    controller = ContractController(db_session)
    contract_data = {
        "id": str(uuid.uuid4()),
        "client_id": str(uuid.uuid4()),  # simulate fake ID for test
        "total_amount": 1000.0,
        "amount_due": 500.0,
        "signed": False,
    }
    contract = controller.create_contract(contract_data)
    assert isinstance(contract, Contract)
    assert contract.total_amount == 1000.0
    assert contract.amount_due == 500.0


def test_get_all_contracts(db_session):
    controller = ContractController(db_session)
    contracts = controller.get_all_contracts()
    assert isinstance(contracts, list)


def test_update_contract(db_session):
    controller = ContractController(db_session)
    contract_data = {
        "id": str(uuid.uuid4()),
        "client_id": str(uuid.uuid4()),
        "total_amount": 1500.0,
        "amount_due": 1500.0,
        "signed": False,
    }
    contract = controller.create_contract(contract_data)

    updated_data = {"amount_due": 0.0, "signed": True}
    updated_contract = controller.update_contract(contract.id, updated_data)
    assert updated_contract.amount_due == 0.0
    assert updated_contract.signed is True


def test_filter_contract_signed_and_paid(db_session):
    controller = ContractController(db_session)
    contract_data = {
        "id": str(uuid.uuid4()),
        "client_id": str(uuid.uuid4()),
        "total_amount": 800.0,
        "amount_due": 0.0,
        "signed": True,
    }
    controller.create_contract(contract_data)
    filtered = controller.filter_contract(signed=True, fully_paid=True)
    assert isinstance(filtered, list)
    assert all(c.signed is True and c.amount_due == 0.0 for c in filtered)


def test_delete_contract(db_session):
    controller = ContractController(db_session)
    contract_data = {
        "id": str(uuid.uuid4()),
        "client_id": str(uuid.uuid4()),
        "total_amount": 600.0,
        "amount_due": 300.0,
        "signed": False,
    }
    contract = controller.create_contract(contract_data)
    result = controller.delete_contract(contract.id)
    assert result is True
