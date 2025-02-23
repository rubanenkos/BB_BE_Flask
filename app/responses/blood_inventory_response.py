from flask import jsonify

class BloodInventoryResponse:

    @staticmethod
    def response_all_records(records):
        inventory_data = [
            {
                "blood_inventory_id": record.blood_inventory_id,
                "blood_bank_id": record.blood_bank_id,
                "blood_part_id": record.blood_part_id,
                "blood_part_name": record.blood_part.name if record.blood_part else None,
                "blood_group_id": record.blood_group_id,
                "blood_group_name": record.blood_group.name if record.blood_group else None,
                "creation_date": record.creation_date.strftime('%Y-%m-%d'),
                "expiry_date": record.expiry_date.strftime('%Y-%m-%d')
            } for record in records
        ]
        return jsonify(inventory_data), 200

    @staticmethod
    def response_find_best_matching_bank(bank_id, total_matched, matched_quantities, missing_quantities):
        from app.models import BloodBank, BloodPart, BloodGroup

        blood_bank = BloodBank.query.get(bank_id)

        def get_names(part_id, group_id):
            blood_part = BloodPart.query.get(part_id)
            blood_group = BloodGroup.query.get(group_id)
            return blood_part.name if blood_part else None, blood_group.name if blood_group else None

        response_data = {
            "bank_id": bank_id,
            "bank_name": blood_bank.name if blood_bank else None,
            "bank_location": blood_bank.location if blood_bank else None,
            "total_matched": total_matched,
            "matched_quantities": [
                {
                    "blood_part_id": int(key.split("_")[0]),
                    "blood_group_id": int(key.split("_")[1]),
                    "quantity": qty,
                    "blood_part_name": get_names(int(key.split("_")[0]), int(key.split("_")[1]))[0],
                    "blood_group_name": get_names(int(key.split("_")[0]), int(key.split("_")[1]))[1],
                } for key, qty in matched_quantities.items()
            ],
            "missing_quantities": [
                {
                    "blood_part_id": int(key.split("_")[0]),
                    "blood_group_id": int(key.split("_")[1]),
                    "missing_quantity": qty,
                    "blood_part_name": get_names(int(key.split("_")[0]), int(key.split("_")[1]))[0],
                    "blood_group_name": get_names(int(key.split("_")[0]), int(key.split("_")[1]))[1],
                } for key, qty in missing_quantities.items()
            ] if missing_quantities else None,
            "status": "partial" if missing_quantities else "complete"
        }
        return jsonify(response_data), 200

    @staticmethod
    def format_daily_report(total_inventory, expiring_tomorrow):
        inventory_summary = {}
        for record in total_inventory:
            key = (record.blood_part_id, record.blood_group_id)
            if key not in inventory_summary:
                inventory_summary[key] = {
                    "blood_part_id": record.blood_part_id,
                    "blood_part_name": record.blood_part.name if record.blood_part else None,
                    "blood_group_id": record.blood_group_id,
                    "blood_group_name": record.blood_group.name if record.blood_group else None,
                    "rhesus_factor": record.blood_group.rhesus_factor if record.blood_group else None,
                    "total_quantity": 0
                }
            inventory_summary[key]["total_quantity"] += 1

        total_inventory_report = list(inventory_summary.values())
        expiring_tomorrow_report = [
            {
                "blood_inventory_id": record.blood_inventory_id,
                "blood_part_id": record.blood_part_id,
                "blood_part_name": record.blood_part.name if record.blood_part else None,
                "blood_group_id": record.blood_group_id,
                "blood_group_name": record.blood_group.name if record.blood_group else None,
                "rhesus_factor": record.blood_group.rhesus_factor if record.blood_group else None,
                "expiry_date": record.expiry_date.strftime('%Y-%m-%d')
            }
            for record in expiring_tomorrow
        ]

        return jsonify({
            "total_inventory": total_inventory_report,
            "expiring_tomorrow": expiring_tomorrow_report
        }), 200