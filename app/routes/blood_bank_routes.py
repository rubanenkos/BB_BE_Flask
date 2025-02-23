from flask import Blueprint, request, jsonify
from app.models import BloodBank

blood_bank_bp = Blueprint('blood_bank', __name__)

@blood_bank_bp.route('/banks', methods=['GET'])
def get_all_banks():
    return BloodBank.get_all_banks()

@blood_bank_bp.route('/bank/<int:blood_bank_id>', methods=['GET'])
def get_bank(blood_bank_id):
    return BloodBank.get_bank_by_id(blood_bank_id)

@blood_bank_bp.route('/create-bank', methods=['POST'])
def create_bank():
    data = request.get_json()
    return BloodBank.create_bank(data)

@blood_bank_bp.route('/update-bank/<int:blood_bank_id>', methods=['PUT'])
def update_bank(blood_bank_id):
    data = request.get_json()
    return BloodBank.update_bank(blood_bank_id, data)