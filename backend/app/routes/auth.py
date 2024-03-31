import bcrypt
from datetime import timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, jwt
from ..models.social import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    registration_date = data.get('registration_date')
    last_seen_date = data.get('last_seen_date')

    user_exists = User.query.filter_by(username=username).first()
    if user_exists:
        return jsonify({"message": "User already exists"}), 400

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
    new_user = User(
        username=username,
        password=hashed_pw.decode('utf-8'),
        email=email,
        registration_date=registration_date,
        last_seen_date=last_seen_date
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_email = data.get('email')
    password = data.get('password')
    username = None
    stored_hashed_password = None

    user_exists = User.query.filter_by(email=user_email).first()
    if user_exists:
        stored_hashed_password = user_exists.password.encode('utf-8')
        username = user_exists.username
        
    if user_exists and bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
        token_tenure = timedelta(days=7)
        access_token = create_access_token(identity=user_email, fresh=True, expires_delta=token_tenure)
        return jsonify({"access_token": access_token, "username": username, "user_email": user_email, "message": "Success"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user_exists = User.query.filter_by(email=current_user).first()
    if user_exists:
        return jsonify(user_exists.serialize()), 200
    return jsonify({"message": "User not found"}), 404

@auth_bp.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_profile():
    current_user = get_jwt_identity()
    user_exists = User.query.filter_by(email=current_user).first()
    if user_exists:
        db.session.delete(user_exists)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"message": "User not found"}), 404
