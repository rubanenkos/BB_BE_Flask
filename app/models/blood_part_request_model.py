from app import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.responses import BloodPartRequestResponse
from app.utils import ErrorHandler
from flask import jsonify

class BloodPartRequest(db.Model):
    __tablename__ = "blood_part_request"

    request_blood_id = Column(Integer, ForeignKey('blood_request.request_blood_id'), primary_key=True)
    blood_part_id = Column(Integer, ForeignKey('blood_part.blood_part_id'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    blood_group_id = Column(Integer, ForeignKey('blood_group.blood_group_id'), primary_key=True)

    blood_request = relationship("BloodRequest", backref=backref("blood_part_requests", lazy=True))
    blood_part = relationship("BloodPart", backref=backref("blood_part_requests", lazy=True))
    blood_group = relationship("BloodGroup", backref=backref("blood_part_list", lazy=True))

    def __repr__(self):
        return f"<BloodPartRequest request_blood_id={self.request_blood_id}, blood_part_id={self.blood_part_id}>"

    @staticmethod
    def get_all_requests_by_request_id(request_blood_id):
        try:
            requests = BloodPartRequest.query.filter_by(request_blood_id=request_blood_id).all()
            print(requests)
            return BloodPartRequestResponse.response_all_requests(requests)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Failed to retrieve blood part requests", status_code=500)

    @staticmethod
    def get_request_by_ids(request_blood_id, blood_part_id):
        try:
            request = BloodPartRequest.query.get((request_blood_id, blood_part_id))
            return BloodPartRequestResponse.response_request(request)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Blood part request not found", status_code=404)

    @staticmethod
    def create_request(data):
        try:
            new_request = BloodPartRequest(
                request_blood_id=data.get("request_blood_id"),
                blood_part_id=data.get("blood_part_id"),
                quantity=data.get("quantity"),
                blood_group_id=data.get("blood_group_id"),
            )
            db.session.add(new_request)
            db.session.commit()
            return {"message": "Blood part request created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to create blood part request", status_code=500)
