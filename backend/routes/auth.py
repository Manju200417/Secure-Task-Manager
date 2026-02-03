from flask import Blueprint, request, jsonify
from models.user import User
from utils.auth_helper import check_password, create_token, token_required, admin_required
from utils.validators import validate_email, validate_password
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check required fields
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    name = data['name']
    email = data['email']
    password = data['password']
    role = data.get('role', 'user')
    
    # Validate email
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate password
    if not validate_password(password):
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Only admin or user roles allowed
    if role not in ['user', 'admin']:
        role = 'user'
    
    # Create user
    user_id = User.create(name, email, password, role)
    
    if not user_id:
        return jsonify({'error': 'Email already exists'}), 400
    
    return jsonify({
        'message': 'User registered successfully',
        'user_id': user_id
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    email = data['email']
    password = data['password']
    
    # Find user
    user = User.find_by_email(email)
    
    if not user:
        logger.warning(f"Failed login attempt - user not found: {email}")
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Check password
    if not check_password(password, user['password']):
        logger.warning(f"Failed login attempt - wrong password: {email}")
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Create token
    token = create_token(user['id'], user['role'])
    
    logger.info(f"User logged in: {email}")
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role']
        }
    }), 200

@auth_bp.route('/users', methods=['GET'])
@token_required
@admin_required
def get_all_users(current_user):
    users = User.get_all()
    
    users_list = []
    for user in users:
        users_list.append({
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role']
        })
    
    return jsonify({'users': users_list}), 200

@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(current_user, user_id):
    user = User.find_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    User.delete(user_id)
    
    return jsonify({'message': 'User deleted successfully'}), 200