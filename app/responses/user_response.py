from flask import jsonify

class UserResponse:
    @staticmethod
    def response_user(user):

        user_data = {
            "user_id": user.user_id,
            "name": user.name if user.name else None,
            "email": user.email,
            "role_id": user.role_id,
        }
        return jsonify(user_data)
