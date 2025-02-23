from flask import Blueprint, request
from app.models import TransportSensor

transport_sensor_bp = Blueprint('transport_sensor', __name__)


@transport_sensor_bp.route('/transport-sensor/<int:blood_transport_id>/<int:blood_fridge_id>', methods=['GET'])
def get_all_sensors(blood_transport_id, blood_fridge_id):
    return TransportSensor.get_all_sensors(blood_transport_id, blood_fridge_id)

@transport_sensor_bp.route('/create-transport-sensor', methods=['POST'])
def create_sensor():
    data = request.get_json()
    return TransportSensor.create_sensor(data)
