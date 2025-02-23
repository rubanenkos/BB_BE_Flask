from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.responses import BloodPartResponse
from app.utils import ErrorHandler

class BloodPart(db.Model):
    __tablename__ = "blood_part"

    blood_part_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    volume_per_bag_ml = Column(Integer, nullable=False)
    shelf_life_days = Column(Integer, nullable=False)
    storage_conditions = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<BloodPart {self.name}>"

    @staticmethod
    def get_all_parts():
        parts = BloodPart.query.all()
        return BloodPartResponse.response_all_parts(parts)

    @staticmethod
    def get_part_by_id(blood_part_id):
        try:
            part = BloodPart.query.get(blood_part_id)
            return BloodPartResponse.response_part(part)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Blood part not found", status_code=404)