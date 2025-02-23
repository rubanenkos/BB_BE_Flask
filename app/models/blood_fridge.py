from app import db
from sqlalchemy import Column, Integer, String
from app.responses import BloodFridgeResponse
from app.utils import ErrorHandler

class BloodFridge(db.Model):
    __tablename__ = "blood_fridge"

    blood_fridge_id = Column(Integer, primary_key=True)
    name_fridge = Column(String(100), nullable=False)
    capacity_ml = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<BloodFridge {self.blood_fridge_id}>"

    @staticmethod
    def get_all_fridges():
        fridges = BloodFridge.query.all()
        return BloodFridgeResponse.response_all_fridges(fridges)

    @staticmethod
    def get_fridge_by_id(blood_fridge_id):
        try:
            fridge = BloodFridge.query.get(blood_fridge_id)
            if not fridge:
                return ErrorHandler.handle_error(None, message="Fridge not found", status_code=404)
            return BloodFridgeResponse.response_fridge(fridge)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Failed to retrieve fridge", status_code=500)

    @staticmethod
    def create_fridge(data):
        try:
            new_fridge = BloodFridge(
                name_fridge=data.get("name_fridge"),
                capacity_ml=data.get("capacity_ml"),
            )
            db.session.add(new_fridge)
            db.session.commit()
            return {"message": "Fridge created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to create fridge", status_code=500)

    @staticmethod
    def update_fridge(blood_fridge_id, data):
        try:
            fridge = BloodFridge.query.get(blood_fridge_id)
            if not fridge:
                return ErrorHandler.handle_error(None, message="Fridge not found", status_code=404)

            fridge.name_fridge = data.get("name_fridge", fridge.name_fridge)
            fridge.capacity_ml = data.get("capacity_ml", fridge.capacity_ml)

            db.session.commit()
            return {"message": "Fridge updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to update fridge", status_code=500)
