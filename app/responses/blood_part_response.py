from flask import jsonify

class BloodPartResponse:
    @staticmethod
    def response_all_parts(parts):
        parts_data = [
            {
                "blood_part_id": part.blood_part_id,
                "name": part.name,
                "volume_per_bag_ml": part.volume_per_bag_ml,
                "shelf_life_days": part.shelf_life_days,
                "storage_conditions": part.storage_conditions,
            }
            for part in parts
        ]
        return jsonify(parts_data)

    @staticmethod
    def response_part(part):
        part_data = {
            "blood_part_id": part.blood_part_id,
            "name": part.name,
            "volume_per_bag_ml": part.volume_per_bag_ml,
            "shelf_life_days": part.shelf_life_days,
            "storage_conditions": part.storage_conditions,
        }
        return jsonify(part_data)
