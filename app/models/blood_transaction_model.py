# from xmlrpc.client import DateTime

from app import db
from sqlalchemy import Column, Integer, String,DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import and_
from sqlalchemy import func, cast, Date
from app.responses import BloodTransactionResponse
from app.utils import ErrorHandler
from datetime import datetime, timedelta

class BloodTransaction(db.Model):
    __tablename__ = "blood_transaction"

    blood_transaction_id = Column(Integer, primary_key=True)
    transaction_type = Column(String(50), nullable=False)  # For example, "incoming", "outgoing"
    supply_id = Column(Integer, ForeignKey('supply.supply_id'), nullable=True)
    request_blood_id = Column(Integer, ForeignKey('blood_request.request_blood_id'), nullable=True)
    blood_part_id = Column(Integer, ForeignKey('blood_part.blood_part_id'), nullable=False)
    quantity = Column(Integer, nullable=True)
    transaction_date = Column(DateTime, nullable=True)
    blood_bank_id = Column(Integer, ForeignKey('blood_bank.blood_bank_id'), nullable=False)

    blood_bank = relationship("BloodBank", backref="transactions")
    blood_part = relationship("BloodPart", backref="transactions")
    request_blood = db.relationship('BloodRequest', backref='transactions')

    def __repr__(self):
        return f"<BloodTransaction ID {self.blood_transaction_id}>"

    @staticmethod
    def get_transactions_by_bank_and_date(blood_bank_id, start_date, end_date):
        print(start_date, end_date)
        try:
            transactions = db.session.query(BloodTransaction).filter(
                (BloodTransaction.blood_bank_id == blood_bank_id) &
                (cast(BloodTransaction.transaction_date, Date) >= start_date) &
                (cast(BloodTransaction.transaction_date, Date) <= end_date)
            ).all()
            print(f"Found {len(transactions)} transactions.")
            return BloodTransactionResponse.response_all_transactions(transactions)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="An error occurred while retrieving transactions",
                                             status_code=500)

    @staticmethod
    def create_transaction( transaction_type, blood_part_id, quantity, blood_bank_id, request_blood_id = None, supply_id = None):
        try:
            new_transaction = BloodTransaction(
                transaction_type=transaction_type,
                supply_id=supply_id,
                blood_part_id=blood_part_id,
                request_blood_id = request_blood_id,
                quantity=quantity,
                transaction_date=datetime.now(),
                blood_bank_id = blood_bank_id
            )
            db.session.add(new_transaction)
            db.session.commit()
            return {"message": "Transaction recorded successfully."}, 201
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="An error occurred while creating the transaction", status_code=500)
