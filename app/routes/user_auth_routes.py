from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app.responses import UserResponse
from app.services import auth_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return User.create_user(data)

@auth_bp.route('/users', methods=['GET'])
def get_all_users():
    return User.get_all_users()

@auth_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_user_id(user_id):
    return User.get_user_by_user_id(user_id)

@auth_bp.route('/user/email', methods=['GET'])
def get_user_by_email():
    user_email = request.args.get('email')
    if not user_email:
        return {"error": "Email parameter is required"}, 400
    return User.get_user_by_user_email(user_email)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return User.authenticate(data)

@auth_bp.route('/user/change-password/<int:user_id>', methods=['POST'])
def change_password(user_id):
    data = request.get_json()

    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return {"error": "Both old_password and new_password are required"}, 400

    return User.change_password(user_id, old_password, new_password)



@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": f"Hello, {user.name}!"}), 200
