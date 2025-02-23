from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from app.responses import DonationSessionResponse
from app.utils import ErrorHandler
from flask import Blueprint, request, jsonify

class DonationSession(db.Model):
    __tablename__ = "donation_session"

    donation_session_id = Column(Integer, primary_key=True)
    donor_id = Column(Integer, ForeignKey('donor.donor_id'), nullable=False)
    donation_date = Column(DateTime, nullable=False)
    quantity_ml = Column(Integer, nullable=False)
    blood_donation_center_id = Column(Integer, ForeignKey('blood_donation_center.blood_donation_center_id'), nullable=False)

    donor = relationship("Donor", backref=backref("donation_sessions", lazy=True))
    blood_donation_center = relationship("BloodDonationCenter", backref=backref("donation_sessions", lazy=True))

    def __repr__(self):
        return f"<DonationSession {self.donation_session_id} - Donor {self.donor_id}>"

    @staticmethod
    def get_sessions_by_donor(donor_id):
        try:
            sessions = DonationSession.query.filter_by(donor_id=donor_id).all()
            return DonationSessionResponse.response_all_sessions(sessions)
        except Exception as e:
            # return ErrorHandler.handle_error(e, message="Sessions not found", status_code=404)
            return jsonify({"error": f"Failed to create user: {str(e)}"}), 500
    @staticmethod
    def create_donation_session(data):
        try:
            new_session = DonationSession(
                donor_id=data.get("donor_id"),
                donation_date=data.get("donation_date"),
                quantity_ml=data.get("quantity_ml"),
                blood_donation_center_id=data.get("blood_donation_center_id"),
            )
            db.session.add(new_session)
            db.session.commit()
            return {"message": "Donation session created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to create donation session", status_code=500)

