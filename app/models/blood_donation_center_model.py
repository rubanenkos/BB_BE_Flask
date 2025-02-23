from app import db
from sqlalchemy import Column, Integer, String

class BloodDonationCenter(db.Model):
    __tablename__ = "blood_donation_center"

    blood_donation_center_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<BloodDonationCenter {self.name}>"
