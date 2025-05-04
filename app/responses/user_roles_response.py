from flask import jsonify

class UserRoleResponse:
    @staticmethod
    def response_all_roles(records):
        roles_data = [
            {
                "role_id": record.role_id,
                "name": record.name,
            } for record in records
        ]
        return jsonify(roles_data), 200
