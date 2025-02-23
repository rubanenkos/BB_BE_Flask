from flask import jsonify

class TransportSensorResponse:
    @staticmethod
    def response_all_sensors(sensors):
        sensor_data = [
            {
                "transport_sensor_id": sensor.transport_sensor_id,
                "blood_fridge_id": sensor.blood_fridge_id,
                "blood_transport_id": sensor.blood_transport_id,
                "temperature": sensor.temperature,
                "time_stamp": sensor.time_stamp,
                "status": sensor.status,
                "blood_fridge_name": sensor.blood_fridge.name_fridge
            }
            for sensor in sensors
        ]
        return jsonify(sensor_data)

    @staticmethod
    def response_sensor(sensor):
        sensor_data = {
            "transport_sensor_id": sensor.transport_sensor_id,
            "blood_fridge_id": sensor.blood_fridge_id,
            "blood_transport_id": sensor.blood_transport_id,
            "temperature": sensor.temperature,
            "time_stamp": sensor.time_stamp,
            "status": sensor.status,
            "blood_fridge_name": sensor.blood_fridge.name_fridge
        }
        return jsonify(sensor_data)
