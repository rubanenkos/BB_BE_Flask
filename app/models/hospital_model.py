from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.responses import HospitalResponse
from app.utils import ErrorHandler

class Hospital(db.Model):
    __tablename__ = "hospital"

    hospital_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    location = Column(String(255), nullable=False)
    contact_number = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)

    user = relationship("User", backref=backref("hospitals", lazy=True))

    def __repr__(self):
        return f"<Hospital {self.name}>"

    @staticmethod
    def get_all_hospitals():
        hospitals = Hospital.query.all()
        return HospitalResponse.response_all_hospitals(hospitals)

    @staticmethod
    def get_hospital_by_id(hospital_id):
        try:
            hospital = Hospital.query.get(hospital_id)
            return HospitalResponse.response_hospital(hospital)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Hospital not found", status_code=404)

    @staticmethod
    def create_hospital(data):
        try:
            new_hospital = Hospital(
                name=data.get("name"),
                email=data.get("email"),
                location=data.get("location"),
                contact_number=data.get("contact_number"),
                user_id=data.get("user_id"),
            )
            db.session.add(new_hospital)
            db.session.commit()
            return {"message": "Hospital created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to create hospital", status_code=500)

    @staticmethod
    def update_hospital(hospital_id, data):
        try:
            hospital = Hospital.query.get(hospital_id)
            if not hospital:
                return ErrorHandler.handle_error(None, message="Hospital not found", status_code=404)

            hospital.name = data.get("name", hospital.name)
            hospital.email = data.get("email", hospital.email)
            hospital.location = data.get("location", hospital.location)
            hospital.contact_number = data.get("contact_number", hospital.contact_number)
            hospital.user_id = data.get("user_id", hospital.user_id)

            db.session.commit()
            return {"message": "Hospital updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to update hospital", status_code=500)
