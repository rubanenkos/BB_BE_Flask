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

@auth_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_user_id(user_id):
    return User.get_user_by_user_id(user_id)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return User.authenticate(data)


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": f"Hello, {user.name}!"}), 200
