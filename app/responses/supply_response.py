from flask import jsonify

class SupplyResponse:
    @staticmethod
    def response_all_supplies(supplies):
        supply_data = [
            {
                "supply_id": supply.supply_id,
                "blood_bank_id": supply.blood_bank_id,
                "blood_bank_name": supply.blood_bank.name if supply.blood_bank else None,
                "blood_donation_center_id": supply.blood_donation_center_id,
                "blood_donation_center_name": supply.blood_donation_center.name if supply.blood_donation_center else None,
                "supply_date": supply.supply_date,
            }
            for supply in supplies
        ]
        return jsonify(supply_data)

    @staticmethod
    def response_supply(supply):

        supply_data = {
            "supply_id": supply.supply_id,
            "blood_bank_id": supply.blood_bank_id,
            "blood_bank_name": supply.blood_bank.name if supply.blood_bank else None,
            "blood_donation_center_id": supply.blood_donation_center_id,
            "blood_donation_center_name": supply.blood_donation_center.name if supply.blood_donation_center else None,
            "supply_date": supply.supply_date,
        }
        return jsonify(supply_data)
