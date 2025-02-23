from flask import jsonify

class SupplyDetailsResponse:
    @staticmethod
    def response_all_details(details_list):
        details_data = [
            {
                "supply_details_id": detail.supply_details_id,
                "supply_id": detail.supply_id,
                "blood_group_id": detail.blood_group_id,
                "blood_group": detail.blood_group.name if detail.blood_group else None,
                "rhesus_factor": detail.blood_group.rhesus_factor if detail.blood_group else None,
                "creation_date": detail.creation_date,
                "expiry_date": detail.expiry_date,
            }
            for detail in details_list
        ]
        return jsonify(details_data)

    @staticmethod
    def response_details(detail):
        details_data = {
            "supply_details_id": detail.supply_details_id,
            "supply_id": detail.supply_id,
            "blood_group_id": detail.blood_group_id,
            "blood_group": detail.blood_group.name if detail.blood_group else None,
            "rhesus_factor": detail.blood_group.rhesus_factor if detail.blood_group else None,
            "creation_date": detail.creation_date,
            "expiry_date": detail.expiry_date,
        }
        return jsonify(details_data)
