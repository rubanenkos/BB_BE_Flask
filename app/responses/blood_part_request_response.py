from flask import jsonify

class BloodPartRequestResponse:
    @staticmethod
    def response_all_requests(requests):
        requests_data = [
            {
                "request_blood_id": request.request_blood_id,
                "blood_part_id": request.blood_part_id,
                "blood_part_name": request.blood_part.name if request.blood_part else None,
                "blood_group_id": request.blood_group_id,
                "quantity": request.quantity,
            }
            for request in requests
        ]
        return jsonify(requests_data)

    @staticmethod
    def response_request(request):
        request_data = {
            "request_blood_id": request.request_blood_id,
            "blood_part_id": request.blood_part_id,
            "blood_part_name": request.blood_part.name if request.blood_part else None,
            "quantity": request.quantity,
        }
        return jsonify(request_data)
