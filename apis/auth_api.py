from flask import Blueprint, request, jsonify, current_app
from models.database import db, User, UserRole
from utils.helpers import hash_password, check_password, generate_token
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    role_value = (data.get('role') or 'farmer').strip().lower()
    if role_value not in [r.value for r in UserRole]:
        role_value = 'farmer'

    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hash_password(data['password']),
        phone=data.get('phone'),
        address=data.get('address'),
        role=UserRole(role_value)
    )
    
    db.session.add(user)
    db.session.commit()
    
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'user_id': user.id,
        'username': user.username,
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.value,
            'phone': user.phone,
            'address': user.address
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('password'):
        return jsonify({'message': 'Missing email/username or password'}), 400

    user = None
    if data.get('username'):
        user = User.query.filter_by(username=data['username']).first()
    elif data.get('email'):
        user = User.query.filter_by(email=data['email']).first()

    if user and user.role is not None and isinstance(user.role, str):
        # Normalize older stored roles if schema changed
        user.role = UserRole(user.role.lower())

    if not user or not check_password(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = generate_token(user.id)

    return jsonify({
        'message': 'Login successful',
        'user_id': user.id,
        'username': user.username,
        'token': token,
        'role': user.role.value,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.value,
            'phone': user.phone,
            'address': user.address
        }
    }), 200

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token missing'}), 401
    
    # In production, verify token properly
    return jsonify({'message': 'User profile endpoint'}), 200
