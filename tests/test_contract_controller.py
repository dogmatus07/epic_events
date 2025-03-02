import pytest
from crm.controllers.contract_controller import ContractController


def test_create_contract(db_session, test_client):
    """
    Test create_contract function
    """
    contract_controller = ContractController(db_session)
    contract_data = {
        "client_id": test_client.id,
        "total_amount": 1000,
        "amount_due": 500,
        "signed": False,
    }
    new_contract = contract_controller.create_contract(contract_data)
    assert new_contract is not None
    assert new_contract.total_amount == 1000
