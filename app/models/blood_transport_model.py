from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from app.utils import ErrorHandler
from app.responses import BloodTransportResponse
from flask import Blueprint, request, jsonify

class BloodTransport(db.Model):
    __tablename__ = "blood_transport"

    blood_transport_id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey("blood_bank.blood_bank_id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    request_blood_id = Column(Integer, ForeignKey("blood_request.request_blood_id"), nullable=False)
    status = Column(String(50), nullable=False)

    bank = relationship("BloodBank", backref=backref("transports", lazy=True))
    user = relationship("User", backref=backref("transports", lazy=True))
    blood_request = relationship("BloodRequest", backref=backref("transports", lazy=True))

    def __repr__(self):
        return f"<BloodTransport {self.blood_transport_id}>"

    @staticmethod
    def get_all_transports(blood_bank_id):
        try:
            transports = BloodTransport.query.filter_by(bank_id=blood_bank_id).all()
            return BloodTransportResponse.response_all_transports(transports)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Failed to fetch transports", status_code=500)

    @staticmethod
    def get_transport_by_id(blood_transport_id):
        try:
            transport = BloodTransport.query.get(blood_transport_id)
            if not transport:
                return ErrorHandler.handle_error(None, message="Transport not found", status_code=404)
            return BloodTransportResponse.response_transport(transport)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Failed to retrieve transport", status_code=500)

    @staticmethod
    def create_transport(data):
        try:
            new_transport = BloodTransport(
                bank_id=data.get("bank_id"),
                start_time=data.get("start_time"),
                end_time=data.get("end_time"),
                user_id=data.get("user_id"),
                request_blood_id=data.get("request_blood_id"),
                status=data.get("status"),
            )
            db.session.add(new_transport)
            db.session.commit()
            return {"message": "Transport created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to create transport", status_code=500)

    @staticmethod
    def update_transport(blood_transport_id, data):
        try:
            transport = BloodTransport.query.get(blood_transport_id)
            if not transport:
                return ErrorHandler.handle_error(None, message="Transport not found", status_code=404)

            transport.bank_id = data.get("bank_id", transport.bank_id)
            transport.start_time = data.get("start_time", transport.start_time)
            transport.end_time = data.get("end_time", transport.end_time)
            transport.user_id = data.get("user_id", transport.user_id)
            transport.request_blood_id = data.get("request_blood_id", transport.request_blood_id)
            transport.status = data.get("status", transport.status)

            db.session.commit()
            return {"message": "Transport updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to update transport", status_code=500)
