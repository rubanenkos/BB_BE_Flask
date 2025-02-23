from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.responses import BloodBankResponse
from app.utils import ErrorHandler

class BloodBank(db.Model):
    __tablename__ = "blood_bank"

    blood_bank_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    location = Column(String(255), nullable=False)
    contact_number = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)

    user = relationship("User", backref=backref("blood_banks", lazy=True))

    def __repr__(self):
        return f"<BloodBank {self.name}>"

    @staticmethod
    def get_all_banks():
        banks = BloodBank.query.all()
        return BloodBankResponse.response_all_banks(banks)

    @staticmethod
    def get_bank_by_id(blood_bank_id):
        try:
            bank = BloodBank.query.get(blood_bank_id)
            return BloodBankResponse.response_bank(bank)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Bank not found", status_code=404)

    @staticmethod
    def create_bank(data):
        try:
            new_bank = BloodBank(
                name=data.get("name"),
                email=data.get("email"),
                location=data.get("location"),
                contact_number=data.get("contact_number"),
                user_id=data.get("user_id"),
            )
            db.session.add(new_bank)
            db.session.commit()
            return {"message": "Blood bank created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to create bank", status_code=500)

    @staticmethod
    def update_bank(blood_bank_id, data):
        try:
            bank = BloodBank.query.get(blood_bank_id)
            if not bank:
                return ErrorHandler.handle_error(None, message="Blood bank not found",status_code=404)

            bank.name = data.get("name", bank.name)
            bank.email = data.get("email", bank.email)
            bank.location = data.get("location", bank.location)
            bank.contact_number = data.get("contact_number", bank.contact_number)
            bank.user_id = data.get("user_id", bank.user_id)

            db.session.commit()
            return {"message": "Blood bank updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to update bank", status_code=500)
