from flask import Blueprint, request, jsonify
from app.models import UserRole

user_role_bp = Blueprint('role', __name__)

@user_role_bp.route('/roles', methods=['GET'])
def get_all_roles():
    return UserRole.get_all_roles()
