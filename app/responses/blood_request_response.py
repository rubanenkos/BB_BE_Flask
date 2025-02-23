from flask import jsonify

class BloodRequestResponse:
    @staticmethod
    def response_all_requests(requests):
        requests_data = [
            {
                "request_blood_id": request.request_blood_id,
                "status": request.status,
                "request_date": request.request_date.isoformat(),
                "hospital_id": request.hospital_id,
                "hospital_name": request.hospital.name if request.hospital else None,
            }
            for request in requests
        ]
        return jsonify(requests_data)

    @staticmethod
    def response_request(request):
        request_data = {
            "request_blood_id": request.request_blood_id,
            "status": request.status,
            "request_date": request.request_date.isoformat(),
            "hospital_id": request.hospital_id,
            "hospital_name": request.hospital.name if request.hospital else None,
        }
        return jsonify(request_data)
