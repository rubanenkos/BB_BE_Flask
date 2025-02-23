from flask import jsonify

class BloodGroupResponse:
    @staticmethod
    def response_all_groups(records):
        group_data = [
            {
                "blood_group_id": record.blood_group_id,
                "name": record.name,
                "rhesus_factor": record.rhesus_factor
            } for record in records
        ]
        return jsonify(group_data), 200

    @staticmethod
    def response_group(record):
        return jsonify({
            "blood_group_id": record.blood_group_id,
            "name": record.name,
            "rhesus_factor": record.rhesus_factor
        }), 200
