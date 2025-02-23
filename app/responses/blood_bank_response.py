from flask import jsonify

class BloodBankResponse:
    @staticmethod
    def response_all_banks(records):
        banks_data = [
            {
                "name": record.name,
                "email": record.email,
                "location": record.location,
                "contact_number": record.contact_number,
                "user_id": record.user_id,
                "user_name": record.user.name if record.user else None
            } for record in records
        ]
        return jsonify(banks_data), 200

    @staticmethod
    def response_bank(record):
        bank_data = {
            "blood_bank_id": record.blood_bank_id,
            "name": record.name,
            "email": record.email,
            "location": record.location,
            "contact_number": record.contact_number,
            "user_id": record.user_id,
            "user_name": record.user.name if record.user else None
        }
        return jsonify(bank_data), 200


