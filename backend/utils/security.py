"""
Security utilities for GradientLab backend.
"""
import re
import logging
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

logger = logging.getLogger(__name__)

def sanitize_input(input_string):
    """
    Sanitize input string to prevent XSS attacks.
    
    Args:
        input_string (str): Input string to sanitize
        
    Returns:
        str: Sanitized string
    """
    if not isinstance(input_string, str):
        return input_string
    
    # Remove script tags
    sanitized = re.sub(r'<script.*?>.*?</script>', '', input_string, flags=re.DOTALL)
    
    # Remove other potentially dangerous tags
    sanitized = re.sub(r'<.*?>', '', sanitized)
    
    # Remove JavaScript event handlers
    sanitized = re.sub(r'on\w+=".*?"', '', sanitized)
    
    return sanitized

def sanitize_json(json_data):
    """
    Recursively sanitize JSON data.
    
    Args:
        json_data (dict or list): JSON data to sanitize
        
    Returns:
        dict or list: Sanitized JSON data
    """
    if isinstance(json_data, dict):
        return {k: sanitize_json(v) for k, v in json_data.items()}
    elif isinstance(json_data, list):
        return [sanitize_json(item) for item in json_data]
    elif isinstance(json_data, str):
        return sanitize_input(json_data)
    else:
        return json_data

def admin_required(fn):
    """
    Decorator to require admin role.
    
    Args:
        fn (function): Function to decorate
        
    Returns:
        function: Decorated function
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Verify JWT
        verify_jwt_in_request()
        
        # Get user ID from JWT
        user_id = get_jwt_identity()
        
        # Import here to avoid circular imports
        from models.user import get_user_by_id
        
        # Get user from database
        user = get_user_by_id(user_id)
        
        # Check if user is admin
        if not user or user.role != 'admin':
            return jsonify({
                'status': 'error',
                'message': 'Admin privileges required'
            }), 403
        
        return fn(*args, **kwargs)
    
    return wrapper

def validate_password_strength(password):
    """
    Validate password strength.
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long'
    
    if not re.search(r'[A-Z]', password):
        return False, 'Password must contain at least one uppercase letter'
    
    if not re.search(r'[a-z]', password):
        return False, 'Password must contain at least one lowercase letter'
    
    if not re.search(r'[0-9]', password):
        return False, 'Password must contain at least one digit'
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, 'Password must contain at least one special character'
    
    return True, 'Password is strong'
