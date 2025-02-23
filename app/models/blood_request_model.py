from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from app.responses import BloodRequestResponse
from app.utils import ErrorHandler
# from app.models import BloodPart

class BloodRequest(db.Model):
    __tablename__ = "blood_request"

    request_blood_id = Column(Integer, primary_key=True)
    status = Column(String(50), nullable=False)
    request_date = Column(DateTime, nullable=False)
    hospital_id = Column(Integer, ForeignKey('hospital.hospital_id'), nullable=False)
    blood_bank_id = Column(Integer, ForeignKey("blood_bank.blood_bank_id"), nullable=True)

    hospital = relationship("Hospital", backref=backref("blood_requests", lazy=True))
    bank = relationship("BloodBank", backref=backref("blood_requests", lazy=True))
    def __repr__(self):
        return f"<BloodRequest {self.request_blood_id}>"

    @staticmethod
    def get_all_requests(blood_bank_id):
        try:
            requests = BloodRequest.query.filter_by(blood_bank_id=blood_bank_id).all()
            return BloodRequestResponse.response_all_requests(requests)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Bank not found", status_code=404)


    @staticmethod
    def get_request_by_id(request_blood_id):
        try:
            request = BloodRequest.query.get(request_blood_id)
            return BloodRequestResponse.response_request(request)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Blood request not found", status_code=404)

    @staticmethod
    def create_request(data):
        try:
            new_request = BloodRequest(
                status=data.get("status"),
                request_date=data.get("request_date"),
                hospital_id=data.get("hospital_id"),
                blood_bank_id = None,
            )
            db.session.add(new_request)
            db.session.commit()
            return {"message": "Blood request created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to create blood request", status_code=500)

    @staticmethod
    def send_request(request_blood_id, blood_bank_id):
        try:
            request_record = db.session.query(BloodRequest).filter_by(request_blood_id=request_blood_id).first()
            request_record.blood_bank_id = blood_bank_id
            request_record.status = "waiting for processing"
            db.session.commit()
            return {"message": "Blood request send successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to create blood request", status_code=500)

    @staticmethod
    def get_pending_requests(blood_bank_id):
        try:

            pending_requests = db.session.query(BloodRequest).filter_by(
                blood_bank_id=blood_bank_id,
                status="waiting for processing"
            ).all()
            return BloodRequestResponse.response_all_requests(pending_requests)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Bank not found", status_code=404)
