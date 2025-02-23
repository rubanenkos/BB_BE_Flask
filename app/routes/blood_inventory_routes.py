from flask import Blueprint, request, jsonify
from app.models import BloodInventory,BloodTransaction

blood_inventory_bp = Blueprint('blood_inventory', __name__)

@blood_inventory_bp.route('/process-supply/<int:supply_id>', methods=['GET'])
def process_supply(supply_id):
    return BloodInventory.process_supply_to_inventory(supply_id)

@blood_inventory_bp.route('/blood-inventory/<int:blood_bank_id>', methods=['GET'])
def get_blood_inventory_by_bank(blood_bank_id):
    return BloodInventory.get_inventory_by_bank_id(blood_bank_id)

@blood_inventory_bp.route('/process-request/<int:blood_bank_id>/<int:request_blood_id>', methods=['GET'])
def process_request(blood_bank_id, request_blood_id):
    return BloodInventory.process_request(blood_bank_id, request_blood_id)

@blood_inventory_bp.route('/transactions/<int:blood_bank_id>/<start_date>/<end_date>', methods=['GET'])
def get_transactions(blood_bank_id,start_date,end_date):
    return BloodTransaction.get_transactions_by_bank_and_date(blood_bank_id, start_date,end_date )

@blood_inventory_bp.route('/find-bank/<int:request_blood_id>', methods=['GET'])
def find_best_matching_bank(request_blood_id):
    return BloodInventory.find_best_matching_bank(request_blood_id)

@blood_inventory_bp.route('/daily-report/<int:blood_bank_id>', methods=['GET'])
def daily_report(blood_bank_id):
    return BloodInventory.generate_daily_report(blood_bank_id)

@blood_inventory_bp.route('/delete-inventory/<int:blood_inventory_id>', methods=['DELETE'])
def delete_inventory(blood_inventory_id):
    return BloodInventory.delete_inventory_by_id(blood_inventory_id)
