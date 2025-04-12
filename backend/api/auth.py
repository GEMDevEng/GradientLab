"""
Authentication API endpoints.
This module handles user authentication and authorization.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import logging
import re

from models.user import get_user_by_username, create_user, get_user_by_id
from utils.security import sanitize_json, validate_password_strength

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    # Sanitize input data
    data = sanitize_json(request.json)

    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400

    # Validate username format
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', data['username']):
        return jsonify({
            'status': 'error',
            'message': 'Username must be 3-20 characters long and contain only letters, numbers, and underscores'
        }), 400

    # Validate email format
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
        return jsonify({
            'status': 'error',
            'message': 'Invalid email format'
        }), 400

    # Validate password strength
    is_valid, error_message = validate_password_strength(data['password'])
    if not is_valid:
        return jsonify({
            'status': 'error',
            'message': error_message
        }), 400

    # Create new user
    user = create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'user'),
        name=data.get('name'),
        bio=data.get('bio')
    )

    if not user:
        return jsonify({
            'status': 'error',
            'message': 'Username or email already exists'
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
    # Sanitize input data
    data = sanitize_json(request.json)

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

    # Check if user exists and password is correct
    if not user or not user.verify_password(data['password']):
        # Log failed login attempt
        logger.warning(f"Failed login attempt for username: {data['username']}")

        return jsonify({
            'status': 'error',
            'message': 'Invalid username or password'
        }), 401

    # Check if user is active
    if not user.is_active:
        logger.warning(f"Login attempt for inactive user: {user.username}")

        return jsonify({
            'status': 'error',
            'message': 'Account is inactive. Please contact an administrator.'
        }), 403

    # Check if 2FA is enabled
    if user.otp_enabled and user.otp_verified:
        # If 2FA is enabled, check if OTP code is provided
        if 'otp_code' not in data:
            # Return partial authentication
            return jsonify({
                'status': 'partial',
                'message': 'Two-factor authentication required',
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'requires_2fa': True
                }
            }), 200

        # Verify OTP code
        if not user.verify_otp(data['otp_code']):
            # Try backup code
            if not user.verify_backup_code(data['otp_code']):
                logger.warning(f"Invalid 2FA code for user: {user.username}")

                return jsonify({
                    'status': 'error',
                    'message': 'Invalid verification code'
                }), 401

    # Create access token
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(days=1)
    )

    # Log successful login
    logger.info(f"User logged in: {user.username}")

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
        logger.warning(f"User not found for ID: {user_id}")
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404

    # Check if user is active
    if not user.is_active:
        logger.warning(f"Inactive user attempted to access profile: {user.username}")
        return jsonify({
            'status': 'error',
            'message': 'Account is inactive. Please contact an administrator.'
        }), 403

    return jsonify({
        'status': 'success',
        'data': user.to_dict()
    }), 200

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change the user's password."""
    # Sanitize input data
    data = sanitize_json(request.json)

    # Validate required fields
    required_fields = ['current_password', 'new_password']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400

    # Get user from JWT token
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)

    if not user:
        logger.warning(f"User not found for ID: {user_id}")
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404

    # Verify current password
    if not user.verify_password(data['current_password']):
        logger.warning(f"Invalid current password for user: {user.username}")
        return jsonify({
            'status': 'error',
            'message': 'Current password is incorrect'
        }), 401

    # Validate new password strength
    is_valid, error_message = validate_password_strength(data['new_password'])
    if not is_valid:
        return jsonify({
            'status': 'error',
            'message': error_message
        }), 400

    # Update password
    user.set_password(data['new_password'])

    # Save user to database
    from config.database import get_session
    session = get_session()
    try:
        session.commit()
        logger.info(f"Password changed for user: {user.username}")

        return jsonify({
            'status': 'success',
            'message': 'Password changed successfully'
        }), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Error changing password: {str(e)}")

        return jsonify({
            'status': 'error',
            'message': 'Error changing password'
        }), 500
    finally:
        session.close()
