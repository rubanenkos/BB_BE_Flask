from app import db
from datetime import datetime, timedelta, date
from sqlalchemy import Column, Integer, Float, ForeignKey, String, Date
from sqlalchemy.orm import relationship, backref
from app.responses import TransportSensorResponse
from app.utils import ErrorHandler
from sqlalchemy import func
from flask import Blueprint, request, jsonify
from app.models import BloodGroup,Supply, SupplyDetails, BloodPart, BloodTransaction, BloodRequest, BloodPartRequest, BloodBank
from app.responses import BloodInventoryResponse

class BloodInventory(db.Model):
    __tablename__ = "blood_inventory"

    blood_inventory_id = Column(Integer, primary_key=True)
    blood_bank_id = Column(Integer, ForeignKey('blood_bank.blood_bank_id'), nullable=False)
    blood_part_id = Column(Integer, ForeignKey('blood_part.blood_part_id'), nullable=False)
    blood_group_id = Column(Integer, ForeignKey('blood_group.blood_group_id'), nullable=False)
    creation_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)

    blood_bank = relationship("BloodBank", backref="blood_inventories")
    blood_part = relationship("BloodPart", backref="blood_inventories")
    blood_group = relationship("BloodGroup", backref=backref("blood_inventory_list", lazy=True))

    def __repr__(self):
        return f"<BloodInventory {self.blood_inventory_id}>"

    @staticmethod
    def get_inventory_by_bank_id(blood_bank_id):
        try:
            records = BloodInventory.query.filter_by(blood_bank_id=blood_bank_id).all()
            return BloodInventoryResponse.response_all_records(records)
        except Exception as e:
            return ErrorHandler.handle_error(e, message="Blood inventory not found", status_code=404)

    @staticmethod
    def process_supply_to_inventory(supply_id):
        try:
            supply = Supply.query.get(supply_id)
            blood_bank_id = supply.blood_bank_id
            supply_details_records = SupplyDetails.get_details_by_supply_id(supply_id)
            blood_parts = BloodPart.query.all()
            total_blood_inventory_records = 0

            for record in supply_details_records:
                for part in blood_parts:
                    expiry_date = record.creation_date + timedelta(days=part.shelf_life_days)

                    new_inventory = BloodInventory(
                        blood_bank_id=record.supply.blood_bank_id,
                        blood_part_id=part.blood_part_id,
                        creation_date=record.creation_date,
                        expiry_date=expiry_date,
                        blood_group_id=record.blood_group_id
                    )
                    db.session.add(new_inventory)
                    db.session.commit()

                total_blood_inventory_records += 1
            for part in blood_parts:
                quantity = total_blood_inventory_records
                BloodTransaction.create_transaction(
                    transaction_type="incoming",
                    supply_id=supply_id,
                    blood_part_id=part.blood_part_id,
                    quantity=quantity,
                    blood_bank_id=blood_bank_id,
                )
                # db.session.commit()
            return {"message": f"Successfully processed {total_blood_inventory_records * len(blood_parts)} blood inventory records"}, 200

        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to processed blood", status_code=500)


    @staticmethod
    def process_request(blood_bank_id, request_blood_id):
        try:
            blood_parts = BloodPart.query.all()
            blood_part_requests = BloodPartRequest.query.filter_by(request_blood_id=request_blood_id).all()
            total_blood_inventory_records = 0

            request = BloodRequest.query.get(request_blood_id)
            if not request:
                return ErrorHandler.handle_error(None, message="Blood request not found", status_code=404)

            request.blood_bank_id = blood_bank_id
            request.status = "In progress"
            db.session.commit()

            for blood_part_request in blood_part_requests:
                quantity_to_remove = blood_part_request.quantity
                blood_part_id = blood_part_request.blood_part_id
                blood_group_id = blood_part_request.blood_group_id

                inventory_records = db.session.query(BloodInventory).filter(
                    BloodInventory.blood_bank_id == blood_bank_id,
                    BloodInventory.blood_part_id == blood_part_id,
                    BloodInventory.blood_group_id == blood_group_id,
                ).order_by(BloodInventory.creation_date.asc()).all()

                removed_records_count = 0

                for inventory in inventory_records:
                    if quantity_to_remove <= 0:
                        break

                    db.session.delete(inventory)
                    quantity_to_remove -= 1
                    removed_records_count += 1

                if quantity_to_remove > 0:
                    db.session.rollback()
                    return ErrorHandler.handle_error(
                        None,
                        message=f"Not enough blood inventory for blood part ID {blood_part_id}. Missing {quantity_to_remove} units.",
                        status_code=400
                    )

                BloodTransaction.create_transaction(
                    transaction_type="outgoing",
                    request_blood_id=request_blood_id,
                    blood_part_id=blood_part_id,
                    quantity=removed_records_count,
                    blood_bank_id=blood_bank_id,
                )

                total_blood_inventory_records += removed_records_count

            db.session.commit()

            return {"message": "Blood request processed successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to process blood request", status_code=500)

    @staticmethod
    def find_best_matching_bank(request_blood_id):
        try:
            blood_part_requests = BloodPartRequest.query.filter_by(request_blood_id=request_blood_id).all()

            required_quantities = {
                f"{req.blood_part_id}_{req.blood_group_id}": req.quantity
                for req in blood_part_requests
            }

            bank_coverage = {}
            blood_banks = BloodBank.query.all()
            for bank in blood_banks:
                bank_id = bank.blood_bank_id
                inventory = BloodInventory.query.filter_by(blood_bank_id=bank_id).all()
                available_quantities = {}

                for inv in inventory:
                    key = f"{inv.blood_part_id}_{inv.blood_group_id}"
                    available_quantities[key] = available_quantities.get(key, 0) + 1

                matched_quantities = {}
                missing_quantities = {}
                for key, req_qty in required_quantities.items():
                    available_qty = available_quantities.get(key, 0)
                    if available_qty >= req_qty:
                        matched_quantities[key] = req_qty
                    else:
                        matched_quantities[key] = available_qty
                        missing_quantities[key] = req_qty - available_qty

                bank_coverage[bank_id] = {
                    "matched_quantities": matched_quantities,
                    "missing_quantities": missing_quantities,
                    "total_matched": sum(matched_quantities.values()),
                }

            best_bank_id, best_bank_data = max(bank_coverage.items(), key=lambda x: x[1]["total_matched"])

            if not best_bank_data["missing_quantities"]:
                return BloodInventoryResponse.response_find_best_matching_bank(
                    best_bank_id,
                    best_bank_data["total_matched"],
                    best_bank_data["matched_quantities"],
                    None
                )

            for blood_part_key, missing_qty in best_bank_data["missing_quantities"].items():
                blood_part_id, blood_group_id = map(int, blood_part_key.split("_"))
                request_record = db.session.query(BloodPartRequest).filter_by(
                    request_blood_id=request_blood_id,
                    blood_part_id=blood_part_id,
                    blood_group_id=blood_group_id
                ).first()

                if request_record:
                    request_record.quantity -= missing_qty

            db.session.commit()

            return BloodInventoryResponse.response_find_best_matching_bank(
                best_bank_id,
                best_bank_data["total_matched"],
                best_bank_data["matched_quantities"],
                best_bank_data["missing_quantities"]
            )

        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(e, message="Failed to find the best matching bank", status_code=500)

    @staticmethod
    def generate_daily_report(blood_bank_id):
        try:
            today = date.today()
            tomorrow = today + timedelta(days=1)
            total_inventory = (
                db.session.query(BloodInventory)
                .filter(BloodInventory.blood_bank_id == blood_bank_id)
                .filter(BloodInventory.expiry_date > today)
                .all()
            )
            expiring_tomorrow = (
                db.session.query(BloodInventory)
                .filter(BloodInventory.blood_bank_id == blood_bank_id)
                .filter(BloodInventory.expiry_date == tomorrow)
                .all()
            )
            return BloodInventoryResponse.format_daily_report(total_inventory, expiring_tomorrow)

        except Exception as e:
            return ErrorHandler.handle_error(e, message="Failed to generate daily report", status_code=500)

    @staticmethod
    def delete_inventory_by_id(blood_inventory_id):
        try:
            record = db.session.query(BloodInventory).filter_by(blood_inventory_id=blood_inventory_id).first()
            db.session.delete(record)
            db.session.commit()
            return jsonify({"message": f"Record with ID {blood_inventory_id} deleted successfully"}), 200

        except Exception as e:
            return ErrorHandler.handle_error(e, message="Failed to delete inventory record", status_code=500)