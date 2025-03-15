from flask import Blueprint, request
from app.models import BloodTransport

blood_transport_bp = Blueprint("blood_transport", __name__)

@blood_transport_bp.route('/blood-transports/<int:blood_bank_id>', methods=['GET'])
def get_all_transports(blood_bank_id):
    return BloodTransport.get_all_transports(blood_bank_id)

@blood_transport_bp.route('/blood-transport/<int:blood_transport_id>', methods=['GET'])
def get_transport_by_id(blood_transport_id):
    return BloodTransport.get_transport_by_id(blood_transport_id)

@blood_transport_bp.route('/blood-transport/user/<int:user_id>', methods=['GET'])
def get_transport_by_user_id(user_id):
    return BloodTransport.get_transport_by_user_id(user_id)

@blood_transport_bp.route('/create-blood-transport', methods=['POST'])
def create_transport():
    data = request.get_json()
    return BloodTransport.create_transport(data)

@blood_transport_bp.route('/update-blood-transport/<int:blood_transport_id>', methods=['PUT'])
def update_transport(blood_transport_id):
    data = request.get_json()
    return BloodTransport.update_transport(blood_transport_id, data)
