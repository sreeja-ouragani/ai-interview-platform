from flask import Blueprint, request, jsonify
from utils.storage import JSONStorage
from config import Config

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/register', methods=['POST'])
def register_user():
    """Register or get user by name"""
    data = request.json
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    # Check if user exists
    existing_user = JSONStorage.get_user(username, Config.USERS_FILE)
    
    if existing_user:
        return jsonify({
            'message': 'Welcome back!',
            'user': existing_user,
            'is_new': False
        }), 200
    
    # Create new user
    user_data = {
        'username': username,
        'experience_level': data.get('experience_level', 'Fresher'),
        'target_role': data.get('target_role', ''),
        'target_company_type': data.get('target_company_type', ''),
        'skills': {
            'technical': [],
            'soft': [],
            'domain': []
        },
        'interview_count': 0,
        'total_score': 0
    }
    
    JSONStorage.save_user(username, user_data, Config.USERS_FILE)
    
    return jsonify({
        'message': 'User registered successfully!',
        'user': user_data,
        'is_new': True
    }), 201

@user_bp.route('/profile/<username>', methods=['GET'])
def get_profile(username):
    """Get user profile"""
    user = JSONStorage.get_user(username, Config.USERS_FILE)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get interview history
    interviews = JSONStorage.get_user_interviews(username, Config.INTERVIEWS_FILE)
    
    return jsonify({
        'user': user,
        'interview_history': interviews
    }), 200

@user_bp.route('/profile/<username>', methods=['PUT'])
def update_profile(username):
    """Update user profile"""
    user = JSONStorage.get_user(username, Config.USERS_FILE)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.json
    
    # Update allowed fields
    if 'experience_level' in data:
        user['experience_level'] = data['experience_level']
    if 'target_role' in data:
        user['target_role'] = data['target_role']
    if 'target_company_type' in data:
        user['target_company_type'] = data['target_company_type']
    
    JSONStorage.save_user(username, user, Config.USERS_FILE)
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': user
    }), 200
