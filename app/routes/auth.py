from flask import Blueprint, jsonify, request, app
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'msg': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'msg': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = str(get_jwt_identity())
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token}), 200
