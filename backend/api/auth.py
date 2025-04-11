"""
Authentication API endpoints.
This module handles user authentication and authorization.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import logging

from models.user import get_user_by_username, create_user, get_user_by_id

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.json
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Create new user
    user = create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'user')
    )
    
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'Username already exists'
        }), 400
    
    # Create access token
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(days=1)
    )
    
    return jsonify({
        'status': 'success',
        'message': 'User registered successfully',
        'data': {
            'user': user.to_dict(),
            'access_token': access_token
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user."""
    data = request.json
    
    # Validate required fields
    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Get user by username
    user = get_user_by_username(data['username'])
    
    if not user or not user.verify_password(data['password']):
        return jsonify({
            'status': 'error',
            'message': 'Invalid username or password'
        }), 401
    
    # Create access token
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(days=1)
    )
    
    return jsonify({
        'status': 'success',
        'message': 'Login successful',
        'data': {
            'user': user.to_dict(),
            'access_token': access_token
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get the current authenticated user."""
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': user.to_dict()
    }), 200
