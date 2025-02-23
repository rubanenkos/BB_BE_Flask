from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

def set_password(password):
    return generate_password_hash(password)

def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)

def generate_access_token(user_id):
    return create_access_token(identity=str(user_id))

