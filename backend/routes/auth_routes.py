from flask import Blueprint, request, jsonify
from models import UserModel
from auth import hash_password, verify_password, generate_token, token_required

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not name or not email or not password:
        return jsonify({'success': False, 'error': 'Name, email, and password are required.'}), 400

    existing_user = UserModel.find_by_email(email)
    if existing_user:
        return jsonify({'success': False, 'error': 'An account with this email already exists.'}), 409

    hashed_pw = hash_password(password)
    user_id = UserModel.create(name, email, hashed_pw)

    return jsonify({
        'success': True,
        'message': 'Registration successful. Please sign in.',
        'user_id': user_id
    }), 201

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password are required.'}), 400

    user = UserModel.find_by_email(email)
    if not user or not verify_password(password, user['password_hash']):
        return jsonify({'success': False, 'error': 'Invalid email or password.'}), 401

    token = generate_token(user['id'], user['email'])

    return jsonify({
        'success': True,
        'token': token,
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user.get('role', 'User')
        }
    }), 200

@auth_bp.route('/api/profile', methods=['GET'])
@token_required
def get_profile():
    user = getattr(request, 'current_user', None)
    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user.get('role', 'User'),
            'created_at': user.get('created_at', '')
        }
    }), 200
