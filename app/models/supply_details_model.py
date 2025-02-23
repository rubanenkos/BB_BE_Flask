from app import db
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.responses import SupplyDetailsResponse
from app.utils import ErrorHandler

class SupplyDetails(db.Model):
    __tablename__ = "supply_details"

    supply_details_id = Column(Integer, primary_key=True)
    supply_id = Column(Integer, ForeignKey("supply.supply_id"), nullable=False)
    blood_group_id = Column(Integer, ForeignKey("blood_group.blood_group_id"), nullable=False)
    creation_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)

    supply = relationship("Supply", backref=backref("details", lazy=True))
    blood_group = relationship("BloodGroup", backref=backref("supply_details", lazy=True))

    def __repr__(self):
        return f"<SupplyDetails ID {self.supply_details_id}>"

    @staticmethod
    def get_all_details(supply_id):
        try:
            details = SupplyDetails.query.filter_by(supply_id=supply_id).all()
            return SupplyDetailsResponse.response_all_details(details)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Failed to fetch supply details", status_code=500)

    @staticmethod
    def get_details_by_id(supply_details_id):
        try:
            details = SupplyDetails.query.get(supply_details_id)
            if not details:
                return ErrorHandler.handle_error(None, message="Supply details not found", status_code=404)
            return SupplyDetailsResponse.response_details(details)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Failed to fetch supply details", status_code=500)

    @staticmethod
    def create_details(data):
        try:
            new_details = SupplyDetails(
                supply_id=data.get("supply_id"),
                blood_group_id=data.get("blood_group_id"),
                creation_date=data.get("creation_date"),
                expiry_date=data.get("expiry_date"),
            )
            db.session.add(new_details)
            db.session.commit()
            return {"message": "Supply details created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            # return ErrorHandler.handle_error(e, message="Failed to create supply details", status_code=500)
            return {"error": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def update_details(supply_details_id, data):
        try:
            details = SupplyDetails.query.get(supply_details_id)
            if not details:
                return ErrorHandler.handle_error(None, message="Supply details not found", status_code=404)

            details.supply_id = data.get("supply_id", details.supply_id)
            details.blood_group_id = data.get("blood_group_id", details.blood_group_id)
            details.creation_date = data.get("creation_date", details.creation_date)
            details.expiry_date = data.get("expiry_date", details.expiry_date)

            db.session.commit()
            return {"message": "Supply details updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            # return ErrorHandler.handle_error(e, message="Failed to update supply details", status_code=500)
            return {"error": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def get_details_by_supply_id(supply_id):
        """Получить записи из supply_details по supply_id."""
        try:
            records = SupplyDetails.query.filter_by(supply_id=supply_id).all()
            if not records:
                return {"error": "No records found for this supply_id"}, 404
            return records
        except Exception as e:
            return {"error": f"An error occurred while fetching supply details: {str(e)}"}, 500