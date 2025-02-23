from app import db
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.responses import SupplyResponse
from app.utils import ErrorHandler
from flask import Blueprint, request, jsonify

class Supply(db.Model):
    __tablename__ = "supply"

    supply_id = Column(Integer, primary_key=True)
    blood_bank_id = Column(Integer, ForeignKey('blood_bank.blood_bank_id'), nullable=False)
    blood_donation_center_id = Column(Integer, ForeignKey('blood_donation_center.blood_donation_center_id'), nullable=False)
    supply_date = Column(Date, nullable=False)

    blood_bank = relationship("BloodBank", backref=backref("supplies", lazy=True))
    blood_donation_center = relationship("BloodDonationCenter", backref=backref("supplies", lazy=True))

    def __repr__(self):
        return f"<Supply ID {self.supply_id} - Date {self.supply_date}>"

    @staticmethod
    def get_all_supplies(blood_bank_id):
        try:
            supplies = Supply.query.filter_by(blood_bank_id=blood_bank_id).all()
            return SupplyResponse.response_all_supplies(supplies)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Bank not found", status_code=404)

    @staticmethod
    def get_supply_by_id(supply_id):
        try:
            supply = Supply.query.get(supply_id)
            return SupplyResponse.response_supply(supply)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Supply not found", status_code=404)

    @staticmethod
    def create_supply(data):
        try:
            new_supply = Supply(
                blood_bank_id=data.get("blood_bank_id"),
                blood_donation_center_id=data.get("blood_donation_center_id"),
                supply_date=data.get("supply_date"),
            )
            db.session.add(new_supply)
            db.session.commit()
            return {"message": "Supply created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to create user: {str(e)}"}), 500
            # return ErrorHandler.handle_error(e, message="Failed to create supply", status_code=500)

    @staticmethod
    def update_supply(supply_id, data):
        try:
            supply = Supply.query.get(supply_id)
            if not supply:
                return ErrorHandler.handle_error(None, message="Supply not found", status_code=404)

            supply.blood_bank_id = data.get("blood_bank_id", supply.blood_bank_id)
            supply.blood_donation_center_id = data.get("blood_donation_center_id", supply.blood_donation_center_id)
            supply.supply_date = data.get("supply_date", supply.supply_date)

            db.session.commit()
            return {"message": "Supply updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to update supply", status_code=500)
