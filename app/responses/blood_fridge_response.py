from flask import jsonify

class BloodFridgeResponse:
    @staticmethod
    def response_all_fridges(fridges):
        fridge_data = [
            {
                "blood_fridge_id": fridge.blood_fridge_id,
                "name_fridge": fridge.name_fridge,
                "capacity_ml": fridge.capacity_ml,
            }
            for fridge in fridges
        ]
        return jsonify(fridge_data)

    @staticmethod
    def response_fridge(fridge):
        fridge_data = {
            "blood_fridge_id": fridge.blood_fridge_id,
            "name_fridge": fridge.name_fridge,
            "capacity_ml": fridge.capacity_ml,
        }
        return jsonify(fridge_data)
