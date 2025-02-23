from flask import Blueprint, request
from app.models import Supply, SupplyDetails

supply_bp = Blueprint('supply', __name__)

@supply_bp.route('/supplies/<int:blood_bank_id>', methods=['GET'])
def get_all_supplies(blood_bank_id):
    return Supply.get_all_supplies(blood_bank_id)

@supply_bp.route('/supply/<int:supply_id>', methods=['GET'])
def get_supply_by_id(supply_id):
    return Supply.get_supply_by_id(supply_id)

@supply_bp.route('/create-supply', methods=['POST'])
def create_supply():
    data = request.get_json()
    return Supply.create_supply(data)

@supply_bp.route('/update-supply/<int:supply_id>', methods=['PUT'])
def update_supply(supply_id):
    data = request.get_json()
    return Supply.update_supply(supply_id, data)

@supply_bp.route('/supply-details/<int:supply_id>', methods=['GET'])
def get_all_supply_details(supply_id):
    return SupplyDetails.get_all_details(supply_id)

@supply_bp.route('/supply-detail/<int:supply_details_id>', methods=['GET'])
def get_supply_details_by_id(supply_details_id):
    return SupplyDetails.get_details_by_id(supply_details_id)

@supply_bp.route('/create-supply-detail', methods=['POST'])
def create_supply_details():
    data = request.get_json()
    return SupplyDetails.create_details(data)

@supply_bp.route('/update-supply-detail/<int:supply_details_id>', methods=['PUT'])
def update_supply_details(supply_details_id):
    data = request.get_json()
    return SupplyDetails.update_details(supply_details_id, data)
