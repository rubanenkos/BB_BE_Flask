from flask import jsonify

class BloodDonationCenterResponse:
    @staticmethod
    def response_all_centers(records):

        centers_data = [
            {
                "name": record.name,
                "blood_donation_center_id": record.blood_donation_center_id,
            } for record in records
        ]
        return jsonify(centers_data), 200
