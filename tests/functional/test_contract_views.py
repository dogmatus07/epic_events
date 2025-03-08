import pytest
from crm.views.contract_views import create_contract


def test_create_contract_view(db_session, test_client, monkeypatch):
    """
    Test create_contract view
    """
    inputs = iter(
        [
            test_client.id,
            "1000",
            "500",
            "y",
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    contract = create_contract(db_session)
    assert contract is not None
    assert contract.total_amount == 1000
