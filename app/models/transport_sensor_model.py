
from app import db
from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime, desc
from sqlalchemy.orm import relationship, backref
from app.responses import TransportSensorResponse
from app.utils import ErrorHandler
from flask import Blueprint, request, jsonify

class TransportSensor(db.Model):
    __tablename__ = "transport_sensor"

    transport_sensor_id = Column(Integer, primary_key=True)
    blood_fridge_id = Column(Integer, ForeignKey('blood_fridge.blood_fridge_id'), nullable=False)
    blood_transport_id = Column(Integer, ForeignKey('blood_transport.blood_transport_id'), nullable=False)
    temperature = Column(Float, nullable=False)
    time_stamp = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)

    blood_fridge = relationship("BloodFridge", backref="transport_sensors")
    blood_transport = relationship("BloodTransport", backref="transport_sensors")

    def __repr__(self):
        return f"<TransportSensor {self.transport_sensor_id}>"

    @staticmethod
    def get_all_sensors(blood_transport_id, blood_fridge_id):
        try:
            if not blood_transport_id or not blood_fridge_id:
                return ErrorHandler.handle_error(
                    None,
                    message="Both blood_transport_id and blood_fridge_id are required",
                    status_code=400
                )
            sensors = TransportSensor.query.filter_by(
                blood_transport_id=blood_transport_id,
                blood_fridge_id=blood_fridge_id
            ).order_by(desc(TransportSensor.time_stamp)).all()
            return TransportSensorResponse.response_all_sensors(sensors)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Failed to fetch transport sensors", status_code=500)

    @staticmethod
    def create_sensor(data):
        try:
            new_sensor = TransportSensor(
                blood_fridge_id=data.get("blood_fridge_id"),
                blood_transport_id=data.get("blood_transport_id"),
                temperature=data.get("temperature"),
                time_stamp=data.get("time_stamp"),
                status=data.get("status")
            )
            db.session.add(new_sensor)
            db.session.commit()
            return {"message": "Transport sensor created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            # return ErrorHandler.handle_error(e, message="Failed to create transport sensor", status_code=500)
            return jsonify({"error": f"Failed to create user: {str(e)}"}), 500

    @staticmethod
    def update_sensor(transport_sensor_id, data):
        try:
            sensor = TransportSensor.query.get(transport_sensor_id)
            if not sensor:
                return ErrorHandler.handle_error(None, message="Transport sensor not found", status_code=404)

            sensor.temperature = data.get("temperature", sensor.temperature)
            sensor.time_stamp = data.get("time_stamp", sensor.time_stamp)
            sensor.status = data.get("status", sensor.status)

            db.session.commit()
            return {"message": "Transport sensor updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to update transport sensor", status_code=500)
