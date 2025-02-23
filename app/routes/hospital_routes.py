from flask import Blueprint, request, jsonify
from app.models import Hospital

hospital_bp = Blueprint('hospital', __name__)

@hospital_bp.route('/hospitals', methods=['GET'])
def get_all_hospitals():
    return Hospital.get_all_hospitals()

@hospital_bp.route('/hospital/<int:hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    return Hospital.get_hospital_by_id(hospital_id)

@hospital_bp.route('/create-hospital', methods=['POST'])
def create_hospital():
    data = request.get_json()
    return Hospital.create_hospital(data)

@hospital_bp.route('/update-hospital/<int:hospital_id>', methods=['PUT'])
def update_hospital(hospital_id):
    data = request.get_json()
    return Hospital.update_hospital(hospital_id, data)
