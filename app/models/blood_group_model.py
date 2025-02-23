from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.responses import BloodGroupResponse
from app.utils import ErrorHandler

class BloodGroup(db.Model):
    __tablename__ = "blood_group"

    blood_group_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    rhesus_factor = Column(String(10), nullable=False)

    # donors = relationship("Donor", backref="blood_group", lazy=True)

    def __repr__(self):
        return f"<BloodGroup {self.name}>"

    @staticmethod
    def get_all_groups():
            groups = BloodGroup.query.all()
            return BloodGroupResponse.response_all_groups(groups)

    @staticmethod
    def get_group_by_id(blood_group_id):
        try:
            group = BloodGroup.query.get(blood_group_id)
            return BloodGroupResponse.response_group(group)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Group not found", status_code=404)
