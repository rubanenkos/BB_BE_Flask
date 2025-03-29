from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from flask_sqlalchemy import SQLAlchemy
from app.responses import UserResponse
from app.services import auth_service
from flask import jsonify
from app.utils import ErrorHandler

class User(db.Model):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey("user_role.role_id"), nullable=False)

    role = db.relationship("UserRole", back_populates="users")

    def set_password(self, password):
        self.password = auth_service.set_password(password)

    @staticmethod
    def authenticate(data):
        user = User.query.filter(
            (User.name == data.get('name')) | (User.email == data.get('email'))
        ).first()

        if not user:
            return ErrorHandler.handle_error(None, message="User not found", status_code=404)

        if not auth_service.check_password(user.password, data.get('password')):
            return ErrorHandler.handle_error(None, message="Invalid credentials", status_code=401)

        access_token = auth_service.generate_access_token(user.user_id)

        return jsonify({ "message": "Login successful", "access_token": access_token}), 200

    @staticmethod
    def get_all_users():
        # users = User.query.all()
        users = User.query.options(joinedload(User.role)).all()
        return UserResponse.response_all_users(users)


    @staticmethod
    def get_user_by_user_id(user_id):
        try:
            user = User.query.filter_by(user_id=user_id).first()
            if not user:
                return {"error": "User not found"}, 404
            return UserResponse.response_user(user)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Failed to fetch user", status_code=500)

    @staticmethod
    def get_user_by_user_email(user_email):
        try:
            user = User.query.filter_by(email=user_email).first()
            if not user:
                return {"error": "User not found"}, 404
            return UserResponse.response_user(user)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Failed to fetch user", status_code=500)

    @staticmethod
    def create_user(data):
        try:
            existing_user = User.query.filter(
                (User.name == data.get('name')) | (User.email == data.get('email'))
            ).first()
            if existing_user:
                return ErrorHandler.handle_error(None, message="User with this name or email already exists", status_code=400)

            new_user = User(
                name=data.get('name'),
                email=data.get('email'),
                role_id=data.get('role_id')
            )
            new_user.set_password(data.get('password'))

            db.session.add(new_user)
            db.session.commit()

            access_token = auth_service.generate_access_token(new_user.user_id)

            return jsonify({ "message": "User registered successfully","access_token": access_token}), 201
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to create user", status_code=500)

