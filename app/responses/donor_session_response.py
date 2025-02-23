from flask import jsonify

class DonationSessionResponse:
    @staticmethod
    def response_all_sessions(sessions):
        session_data = [
            {
                "donation_session_id": session.donation_session_id,
                "donor_id": session.donor_id,
                "donor_name": session.donor.user.name if session.donor and session.donor.user else None,
                "donation_date": session.donation_date,
                "quantity_ml": session.quantity_ml,
                "blood_donation_center_id": session.blood_donation_center_id,
                "blood_donation_center_name": session.blood_donation_center.name if session.blood_donation_center else None,
            }
            for session in sessions
        ]
        return jsonify(session_data)

    @staticmethod
    def response_session(session):
        session_data = {
            "donation_session_id": session.donation_session_id,
            "donor_id": session.donor_id,
            "donor_name": session.donor.user.name if session.donor and session.donor.user else None,
            "donation_date": session.donation_date,
            "quantity_ml": session.quantity_ml,
            "blood_donation_center_id": session.blood_donation_center_id,
            "blood_donation_center_name": session.blood_donation_center.name if session.blood_donation_center else None,
        }
        return jsonify(session_data)
