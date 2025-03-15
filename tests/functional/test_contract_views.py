import pytest
from crm.views.contract_views import create_contract


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
