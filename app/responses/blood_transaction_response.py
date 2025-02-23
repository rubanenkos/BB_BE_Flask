from flask import jsonify

class BloodTransactionResponse:
    @staticmethod
    def response_all_transactions(transactions):
        transactions_data = [
            {
                "transaction_id": transaction.blood_transaction_id,
                "transaction_type": transaction.transaction_type,
                "quantity": transaction.quantity,
                "blood_part_id": transaction.blood_part_id,
                "blood_part_name": transaction.blood_part.name if transaction.blood_part else None,
                "transaction_date": transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S') if transaction.transaction_date else None,
                "request_blood_id": transaction.request_blood_id,
                "supply_id": transaction.supply_id,
            }
            for transaction in transactions
        ]
        return jsonify(transactions_data), 200

    @staticmethod
    def response_single_transaction(transaction):
        transaction_data = {
            "transaction_id": transaction.blood_transaction_id,
            "transaction_type": transaction.transaction_type,
            "quantity": transaction.quantity,
            "blood_part_id": transaction.blood_part_id,
            "blood_part_name": transaction.blood_part.name if transaction.blood_part else None,
            "transaction_date": transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S') if transaction.transaction_date else None,
            "request_blood_id": transaction.request_blood_id,
            "supply_id": transaction.supply_id,
        }
        return jsonify(transaction_data), 200
