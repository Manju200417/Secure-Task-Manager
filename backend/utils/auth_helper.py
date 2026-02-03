import jwt
import bcrypt
from datetime import datetime, timedelta
from config import Config
from functools import wraps
from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRY_HOURS)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Decorator to protect routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            logger.warning("Missing token in request")
            return jsonify({'error': 'Token is missing'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = decode_token(token)
        if not payload:
            logger.warning("Invalid or expired token")
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Pass user info to the route
        return f(payload, *args, **kwargs)
    
    return decorated

# Decorator to check admin role
def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user['role'] != 'admin':
            logger.warning(f"Unauthorized admin access attempt by user {current_user['user_id']}")
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(current_user, *args, **kwargs)
    
    return decorated