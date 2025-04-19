import re
from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True)
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not all([username, password, email]):
        return jsonify({'error': 'Username, email, and password are required'}), 400

    if len(username) < 4:
        return jsonify({'error': 'Username must be at least 4 characters'}), 400

    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    try:
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': new_user.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful'}), 200