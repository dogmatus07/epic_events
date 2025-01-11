from crm.models.models import Contract
from crm.db.session import SessionLocal


class ContractController:
    """
    Controller class for Contract model.
    """

    @staticmethod
    def get_all_contracts():
        """
        Get all contracts from the database.
        """
        db = SessionLocal()
        contracts = db.query(Contract).all()
        db.close()
        return contracts

    @staticmethod
    def create_contract(client_email, total_amount, amount_due, signed, commercial_id):
        """
        Create a new contract.
        """

        db = SessionLocal()
        contract = Contract(
            client_email=client_email,
            total_amount=total_amount,
            amount_due=amount_due,
            signed=signed,
            commercial_id=commercial_id,
        )
        db.add(contract)
        db.commit()
        db.close()
        return contract

    @staticmethod
    def udpate_contract(
        contract_id, client_email, total_amount, amount_due, signed, commercial_id
    ):
        """
        Update a contract.
        """
        db = SessionLocal()
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        contract.client_email = client_email
        contract.total_amount = total_amount
        contract.amount_due = amount_due
        contract.signed = signed
        contract.commercial_id = commercial_id
        db.commit()
        db.close()
        return contract

    @staticmethod
    def delete_contract(contract_id):
        """
        Delete a contract.
        """
        db = SessionLocal()
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        db.delete(contract)
        db.commit()
        db.close()
        return contract
