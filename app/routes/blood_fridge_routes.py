from flask import Blueprint, request
from app.models import BloodFridge

blood_fridge_bp = Blueprint("blood_fridge", __name__)

@blood_fridge_bp.route('/blood-fridges', methods=['GET'])
def get_all_fridges():
    return BloodFridge.get_all_fridges()

@blood_fridge_bp.route('/blood-fridge/<int:blood_fridge_id>', methods=['GET'])
def get_fridge_by_id(blood_fridge_id):
    return BloodFridge.get_fridge_by_id(blood_fridge_id)

@blood_fridge_bp.route('/create-blood-fridge', methods=['POST'])
def create_fridge():
    data = request.get_json()
    return BloodFridge.create_fridge(data)

@blood_fridge_bp.route('/update-blood-fridge/<int:blood_fridge_id>', methods=['PUT'])
def update_fridge(blood_fridge_id):
    data = request.get_json()
    return BloodFridge.update_fridge(blood_fridge_id, data)
