from flask import jsonify

class DonorResponse:
    @staticmethod
    def response_all_donors(donors):

        donor_data = [
            {
                "donor_id": donor.donor_id,
                "user_id": donor.user_id,
                "user_name": donor.user.name if donor.user else None,
                "blood_group_id": donor.blood_group_id,
                "blood_group": donor.blood_group.name if donor.blood_group else None,
                "rhesus_factor": donor.blood_group.rhesus_factor if donor.blood_group else None,
                "contact_number": donor.contact_number,
                "sex": donor.sex,
                "date_of_birth": donor.date_of_birth,
                "age": donor.age,
            }
            for donor in donors
        ]
        return jsonify(donor_data)

    @staticmethod
    def response_donor(donor):

        donor_data = {
            "donor_id": donor.donor_id,
            "user_id": donor.user_id,
            "user_name": donor.user.name if donor.user else None,
            "blood_group_id": donor.blood_group_id,
            "blood_group": donor.blood_group.name if donor.blood_group else None,
            "rhesus_factor": donor.blood_group.rhesus_factor if donor.blood_group else None,
            "contact_number": donor.contact_number,
            "sex": donor.sex,
            "date_of_birth": donor.date_of_birth,
            "age": donor.age,
        }
        return jsonify(donor_data)
