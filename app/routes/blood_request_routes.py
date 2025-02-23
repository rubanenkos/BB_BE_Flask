from flask import Blueprint, request
from app.models import BloodRequest, BloodPartRequest, BloodInventory

blood_request_bp = Blueprint('blood_request', __name__)

@blood_request_bp.route('/blood-requests/<int:blood_bank_id>', methods=['GET'])
def get_all_blood_requests(blood_bank_id):
    return BloodRequest.get_all_requests(blood_bank_id)

@blood_request_bp.route('/blood-request/<int:request_blood_id>', methods=['GET'])
def get_blood_request_by_id(request_blood_id):
    return BloodRequest.get_request_by_id(request_blood_id)

@blood_request_bp.route('/create-blood-request', methods=['POST'])
def create_blood_request():
    data = request.get_json()
    return BloodRequest.create_request(data)

@blood_request_bp.route('/update-blood-request/<int:request_blood_id>', methods=['PUT'])
def update_blood_request(request_blood_id):
    data = request.get_json()
    return BloodRequest.update_request(request_blood_id, data)

@blood_request_bp.route('/blood-part-requests/<int:request_blood_id>', methods=['GET'])
def get_all_blood_part_requests_by_request_id(request_blood_id):
    return BloodPartRequest.get_all_requests_by_request_id(request_blood_id)


@blood_request_bp.route('/blood-part-request/<int:request_blood_id>/<int:blood_part_id>', methods=['GET'])
def get_blood_part_request(request_blood_id, blood_part_id):
    return BloodPartRequest.get_request_by_ids(request_blood_id, blood_part_id)

@blood_request_bp.route('/create-blood-part-request', methods=['POST'])
def create_blood_part_request():
    data = request.get_json()
    return BloodPartRequest.create_request(data)

@blood_request_bp.route('/send-request/<int:request_blood_id>/<int:blood_bank_id>', methods=['GET'])
def send_request(request_blood_id, blood_bank_id):
    return BloodRequest.send_request(request_blood_id, blood_bank_id)


@blood_request_bp.route('/pending-requests/<int:blood_bank_id>', methods=['GET'])
def get_pending_requests(blood_bank_id):
    return BloodRequest.get_pending_requests(blood_bank_id)
