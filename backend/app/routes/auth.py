import bcrypt
from datetime import timedelta
from flask import Blueprint, jsonify, request
from app import db, jwt
from ..models.social import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    registration_date = data.get('registration_date')
    last_seen_date = data.get('last_seen_date')

    userexists = User.query.filter_by(username=username).first()
    
    if userexists is not None:
        return jsonify({"message": "User already exists"}), 400

    hashedpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
    new_user = User(
        username=username,
        password=hashedpw.decode('utf-8'),
        email=email,
        registration_date=registration_date,
        last_seen_date=last_seen_date
    )
    print(hashedpw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    useremail = data.get('email')
    password = data.get('password')
    username = None
    stored_hashed_password = None
    #useremail = None

    userexists = User.query.filter_by(email=useremail).first()
    if userexists:
        stored_hashed_password = userexists.password.encode('utf-8')
        username = userexists.username
        
    if userexists != None and bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
        token_tenure = timedelta(days=7)
        access_token = create_access_token(identity=useremail, fresh=True, expires_delta=token_tenure)
        return jsonify({"access_token": access_token, "username": username, "useremail": useremail, "message": "Success"}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    # You can fetch user data from your database here
    return jsonify({"message": f"Welcome, {current_user}!"}), 200