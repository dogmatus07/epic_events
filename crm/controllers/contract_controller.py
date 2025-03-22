from sqlalchemy.orm import Session
from crm.models.models import Contract


class ContractController:
    """
    Controller class for Contract model.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_contracts(self):
        """
        Get all contracts from the database.
        """
        return self.db_session.query(Contract).all()

    def create_contract(self, contract_data):
        """
        Create a new contract.
        """
        new_contract = Contract(**contract_data)
        self.db_session.add(new_contract)
        self.db_session.commit()
        return new_contract

    def update_contract(self, contract_id, updated_data):
        """
        Update a contract.
        """
        contract = self.db_session.get(Contract, contract_id)
        if not contract:
            return None
        for key, value in updated_data.items():
            setattr(contract, key, value)
        self.db_session.commit()

        return contract

    def filter_contract(self, signed=None, fully_paid=None):
        """
        Filter contracts based on the fact that they are signed or fully paid.
        :param signed: bool | None -> True (signés), False (non signés), None (tous)
        :param fully_paid: bool | None -> True (payés), False (non payés), None (tous)
        """
        query = self.db_session.query(Contract)
        if signed is not None:
            query = query.filter(Contract.signed == signed)
        if fully_paid is not None:
            query = query.filter(Contract.amount_due == 0 if fully_paid else Contract.amount_due > 0)

        return query.all()

    def delete_contract(self, contract_id):
        """
        Delete a contract.
        """
        contract = self.db_session.get(Contract, contract_id)
        if not contract:
            return None
        self.db_session.delete(contract)
        self.db_session.commit()
        return True
