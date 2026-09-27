import datetime
import functools
import jwt
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import UserModel

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)

def generate_token(user_id: int, email: str) -> str:
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm='HS256')

def decode_token(token: str):
    try:
        return jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def extract_token_from_header() -> str:
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header.split(' ', 1)[1].strip()
    return ''

def get_optional_user():
    """Returns the user dict if a valid token is passed; otherwise None."""
    token = extract_token_from_header()
    if not token:
        return None
    payload = decode_token(token)
    if not payload:
        return None
    return UserModel.find_by_id(payload.get('user_id'))

def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = extract_token_from_header()
        if not token:
            return jsonify({'success': False, 'error': 'Authorization token is missing'}), 401
        
        payload = decode_token(token)
        if not payload:
            return jsonify({'success': False, 'error': 'Token is invalid or expired'}), 401
        
        current_user = UserModel.find_by_id(payload.get('user_id'))
        if not current_user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        request.current_user = current_user
        return f(*args, **kwargs)
    return decorated
