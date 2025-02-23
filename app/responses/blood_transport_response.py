from flask import jsonify

class BloodTransportResponse:
    @staticmethod
    def response_all_transports(transports):
        transport_data = [
            {
                "blood_transport_id": transport.blood_transport_id,
                "bank_id": transport.bank_id,
                "bank_name": transport.bank.name if transport.bank else None,
                "start_time": transport.start_time,
                "end_time": transport.end_time,
                "user_id": transport.user_id,
                "user_name": transport.user.name if transport.user else None,
                "request_blood_id": transport.request_blood_id,
                "hospital_name": transport.blood_request.hospital.name if transport.blood_request and transport.blood_request.hospital else None,
                "status": transport.status,
            }
            for transport in transports
        ]
        return jsonify(transport_data)

    @staticmethod
    def response_transport(transport):
        transport_data = {
            "blood_transport_id": transport.blood_transport_id,
            "bank_id": transport.bank_id,
            "bank_name": transport.bank.name if transport.bank else None,
            "start_time": transport.start_time,
            "end_time": transport.end_time,
            "user_id": transport.user_id,
            "user_name": transport.user.name if transport.user else None,
            "request_blood_id": transport.request_blood_id,
            "hospital_name": transport.blood_request.hospital.name if transport.blood_request and transport.blood_request.hospital else None,
            "status": transport.status,
        }
        return jsonify(transport_data)
