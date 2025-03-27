from sqlalchemy.orm import Session
from crm.models.models import Contract
from sentry_sdk import capture_exception
from rich.console import Console

console = Console()


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
        try:
            new_contract = Contract(**contract_data)
            self.db_session.add(new_contract)
            self.db_session.commit()
            return new_contract
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de la création du contrat")
            return None


    def update_contract(self, contract_id, updated_data):
        """
        Update a contract.
        """
        try:
            contract = self.db_session.get(Contract, contract_id)
            if not contract:
                return None
            for key, value in updated_data.items():
                setattr(contract, key, value)
            self.db_session.commit()
            return contract
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de la mise à jour du contrat")
            return None

    def filter_contract(self, signed=None, fully_paid=None):
        """
        Filter contracts based on the fact that they are signed or fully paid.
        :param signed: bool | None -> True (signés), False (non signés), None (tous)
        :param fully_paid: bool | None -> True (payés), False (non payés), None (tous)
        """
        try:
            query = self.db_session.query(Contract)
            if signed is not None:
                query = query.filter(Contract.signed == signed)
            if fully_paid is not None:
                query = query.filter(Contract.amount_due == 0 if fully_paid else Contract.amount_due > 0)
            return query.all()
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors du filtrage des contrats")
            return None

    def delete_contract(self, contract_id):
        """
        Delete a contract.
        """
        try:
            contract = self.db_session.get(Contract, contract_id)
            if not contract:
                return None
            self.db_session.delete(contract)
            self.db_session.commit()
            return True
        except Exception as e:
            capture_exception(e)
            console.print("Erreur lors de la suppression du contrat")
            return None
