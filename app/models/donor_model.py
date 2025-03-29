from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Computed
from sqlalchemy.orm import relationship, backref
from app.responses import DonorResponse
from app.utils import ErrorHandler
from flask import Blueprint, request, jsonify

class Donor(db.Model):
    __tablename__ = "donor"

    donor_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    blood_group_id = Column(Integer, ForeignKey('blood_group.blood_group_id'), nullable=False)
    contact_number = Column(String(50), nullable=False)
    sex = Column(String(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    age = Column(Integer, Computed("(datediff(year, [Date_of_birth], getdate()))"), nullable=True)

    user = relationship("User", backref=backref("donors", lazy=True))
    blood_group = relationship("BloodGroup", backref=backref("donors", lazy=True))

    def __repr__(self):
        return f"<Donor {self.donor_id}>"

    @staticmethod
    def get_all_donors():
        donors = Donor.query.all()
        return DonorResponse.response_all_donors(donors)

    @staticmethod
    def get_donor_by_user_id(user_id):
        try:
            donor = Donor.query.filter_by(user_id=user_id).first()
            if not donor:
                return {"error": "Donor not found"}, 404
            return DonorResponse.response_donor(donor)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Failed to fetch donor", status_code=500)

    @staticmethod
    def create_donor(data):
        try:
            print(data)
            new_donor = Donor(
                user_id=data.get("user_id"),
                blood_group_id=data.get("blood_group_id"),
                contact_number=data.get("contact_number"),
                sex=data.get("sex"),
                date_of_birth=data.get("date_of_birth"),
            )
            db.session.add(new_donor)
            db.session.commit()
            return {"message": "Donor created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to create donor", status_code=500)


    @staticmethod
    def update_donor(user_id, data):
        try:
            donor = Donor.query.filter_by(user_id=user_id).first()
            if not donor:
                return ErrorHandler.handle_error(None, message="Donor not found", status_code=404)

            donor.blood_group_id = data.get("blood_group_id", donor.blood_group_id)
            donor.contact_number = data.get("contact_number", donor.contact_number)
            donor.sex = data.get("sex", donor.sex)
            donor.date_of_birth = data.get("date_of_birth", donor.date_of_birth)

            db.session.commit()
            return {"message": "Donor updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to update donor", status_code=500)

    @staticmethod
    def update_donor_phone(user_id, data):
        try:
            donor = Donor.query.filter_by(user_id=user_id).first()
            if not donor:
                return ErrorHandler.handle_error(None, message="Donor not found", status_code=404)

            contact_number = data.get("contact_number")
            if contact_number is not None:
                donor.contact_number = contact_number

            db.session.commit()
            return {"message": "Donor phone number updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to update donor phone number", status_code=500)