from sqlalchemy.orm import Session
from crm.models.models import Contract


class ContractController():
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
        contract = self.db_session.query(Contract).get(contract_id)
        if not contract:
            return None
        for key, value in updated_data.items():
            setattr(contract, key, value)
        self.db_session.commit()

        return contract

    def delete_contract(self, contract_id):
        """
        Delete a contract.
        """
        contract = self.db_session.query(Contract).get(contract_id)
        if not contract:
            return None
        self.db_session.delete(contract)
        self.db_session.commit()
        return True
