from flask import Blueprint, request, jsonify
from app.models import BloodDonationCenter

centers_bp = Blueprint('centers', __name__)

@centers_bp.route('/centers', methods=['GET'])
def get_all_centers():
    return BloodDonationCenter.get_all_centers()