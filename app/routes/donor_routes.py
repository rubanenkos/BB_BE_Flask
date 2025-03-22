from flask import Blueprint, request
from app.models import Donor, DonationSession

donor_bp = Blueprint('donor', __name__)

@donor_bp.route('/donors', methods=['GET'])
def get_all_donors():
    return Donor.get_all_donors()

@donor_bp.route('/donor/<int:user_id>', methods=['GET'])
def get_donor_by_user_id(user_id):
    return Donor.get_donor_by_user_id(user_id)

@donor_bp.route('/create-donor', methods=['POST'])
def create_donor():
    data = request.get_json()
    return Donor.create_donor(data)

@donor_bp.route('/update-donor/<int:donor_id>', methods=['PUT'])
def update_donor(donor_id):
    data = request.get_json()
    return Donor.update_donor(donor_id, data)

@donor_bp.route('/update-donor/phone/<int:user_id>', methods=['PUT'])
def update_donor_phone(user_id):
    data = request.get_json()
    return Donor.update_donor_phone(user_id, data)

@donor_bp.route('/donation-session/<int:donor_id>', methods=['GET'])
def get_donation_sessions_by_donor_id(donor_id):
    return DonationSession.get_sessions_by_donor(donor_id)

@donor_bp.route('/create-donation-session', methods=['POST'])
def create_donation_session():
    data = request.get_json()
    return DonationSession.create_donation_session(data)
