from flask import Blueprint, request, jsonify
from app.models import BloodGroup, BloodPart

blood_group_bp = Blueprint('blood_group', __name__)

@blood_group_bp.route('/blood-groups', methods=['GET'])
def get_all_groups():
    return BloodGroup.get_all_groups()

@blood_group_bp.route('/blood-group/<int:blood_group_id>', methods=['GET'])
def get_group(blood_group_id):
    return BloodGroup.get_group_by_id(blood_group_id)

@blood_group_bp.route('/blood-parts', methods=['GET'])
def get_all_blood_parts():
    return BloodPart.get_all_parts()

@blood_group_bp.route('/blood-part/<int:blood_part_id>', methods=['GET'])
def get_blood_part_by_id(blood_part_id):
    return BloodPart.get_part_by_id(blood_part_id)