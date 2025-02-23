from app.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity



db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    from app.routes import auth_bp, blood_bank_bp, hospital_bp, blood_group_bp, donor_bp, supply_bp, blood_request_bp, blood_transport_bp, blood_fridge_bp, transport_sensor_bp, blood_inventory_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(blood_bank_bp)
    app.register_blueprint(hospital_bp)
    app.register_blueprint(blood_group_bp)
    app.register_blueprint(donor_bp)
    app.register_blueprint(supply_bp)
    app.register_blueprint(blood_request_bp)
    app.register_blueprint(blood_transport_bp)
    app.register_blueprint(blood_fridge_bp)
    app.register_blueprint(transport_sensor_bp)
    app.register_blueprint(blood_inventory_bp)
    return app