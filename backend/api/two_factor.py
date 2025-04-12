"""
Two-factor authentication API for GradientLab backend.
"""
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
import pyotp
import qrcode
import io
import json
from datetime import datetime, timedelta

from models.user import get_user_by_id
from config.database import get_session

logger = logging.getLogger(__name__)

# Create blueprint
two_factor_bp = Blueprint('two_factor', __name__)

@two_factor_bp.route('/setup', methods=['POST'])
@jwt_required()
def setup_2fa():
    """Set up two-factor authentication for the user."""
    user_id = get_jwt_identity()
    
    # Get user from database
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    # Generate OTP secret
    otp_secret = user.generate_otp_secret()
    
    # Save user to database
    session = get_session()
    try:
        session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Two-factor authentication setup initiated',
            'data': {
                'secret': otp_secret,
                'uri': user.get_otp_uri()
            }
        }), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Error setting up 2FA: {str(e)}")
        
        return jsonify({
            'status': 'error',
            'message': 'Error setting up two-factor authentication'
        }), 500
    finally:
        session.close()

@two_factor_bp.route('/qrcode', methods=['GET'])
@jwt_required()
def get_qrcode():
    """Get QR code for two-factor authentication setup."""
    user_id = get_jwt_identity()
    
    # Get user from database
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    # Check if user has OTP secret
    if not user.otp_secret:
        return jsonify({
            'status': 'error',
            'message': 'Two-factor authentication not set up'
        }), 400
    
    # Get OTP URI
    uri = user.get_otp_uri()
    if not uri:
        return jsonify({
            'status': 'error',
            'message': 'Error generating QR code'
        }), 500
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save image to memory
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

@two_factor_bp.route('/verify', methods=['POST'])
@jwt_required()
def verify_2fa():
    """Verify two-factor authentication code."""
    user_id = get_jwt_identity()
    data = request.json
    
    # Validate required fields
    if 'code' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required field: code'
        }), 400
    
    # Get user from database
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    # Check if user has OTP secret
    if not user.otp_secret:
        return jsonify({
            'status': 'error',
            'message': 'Two-factor authentication not set up'
        }), 400
    
    # Verify OTP code
    if user.verify_otp(data['code']):
        # Update user in database
        session = get_session()
        try:
            user.otp_verified = True
            user.otp_enabled = True
            
            # Generate backup codes if not already generated
            if not user.backup_codes:
                user.generate_backup_codes()
            
            session.commit()
            
            # Get backup codes
            backup_codes = json.loads(user.backup_codes) if user.backup_codes else []
            
            return jsonify({
                'status': 'success',
                'message': 'Two-factor authentication verified',
                'data': {
                    'backup_codes': backup_codes
                }
            }), 200
        except Exception as e:
            session.rollback()
            logger.error(f"Error verifying 2FA: {str(e)}")
            
            return jsonify({
                'status': 'error',
                'message': 'Error verifying two-factor authentication'
            }), 500
        finally:
            session.close()
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid verification code'
        }), 400

@two_factor_bp.route('/disable', methods=['POST'])
@jwt_required()
def disable_2fa():
    """Disable two-factor authentication."""
    user_id = get_jwt_identity()
    data = request.json
    
    # Validate required fields
    if 'code' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required field: code'
        }), 400
    
    # Get user from database
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    # Check if user has OTP enabled
    if not user.otp_enabled:
        return jsonify({
            'status': 'error',
            'message': 'Two-factor authentication not enabled'
        }), 400
    
    # Verify OTP code or backup code
    valid = user.verify_otp(data['code'])
    if not valid:
        valid = user.verify_backup_code(data['code'])
    
    if valid:
        # Update user in database
        session = get_session()
        try:
            user.otp_secret = None
            user.otp_enabled = False
            user.otp_verified = False
            user.backup_codes = None
            
            session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Two-factor authentication disabled'
            }), 200
        except Exception as e:
            session.rollback()
            logger.error(f"Error disabling 2FA: {str(e)}")
            
            return jsonify({
                'status': 'error',
                'message': 'Error disabling two-factor authentication'
            }), 500
        finally:
            session.close()
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid verification code'
        }), 400

@two_factor_bp.route('/backup-codes', methods=['GET'])
@jwt_required()
def get_backup_codes():
    """Get backup codes for two-factor authentication."""
    user_id = get_jwt_identity()
    
    # Get user from database
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    # Check if user has OTP enabled
    if not user.otp_enabled:
        return jsonify({
            'status': 'error',
            'message': 'Two-factor authentication not enabled'
        }), 400
    
    # Get backup codes
    backup_codes = json.loads(user.backup_codes) if user.backup_codes else []
    
    return jsonify({
        'status': 'success',
        'data': {
            'backup_codes': backup_codes
        }
    }), 200

@two_factor_bp.route('/backup-codes/regenerate', methods=['POST'])
@jwt_required()
def regenerate_backup_codes():
    """Regenerate backup codes for two-factor authentication."""
    user_id = get_jwt_identity()
    data = request.json
    
    # Validate required fields
    if 'code' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required field: code'
        }), 400
    
    # Get user from database
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    # Check if user has OTP enabled
    if not user.otp_enabled:
        return jsonify({
            'status': 'error',
            'message': 'Two-factor authentication not enabled'
        }), 400
    
    # Verify OTP code
    if user.verify_otp(data['code']):
        # Update user in database
        session = get_session()
        try:
            # Generate new backup codes
            backup_codes = user.generate_backup_codes()
            
            session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Backup codes regenerated',
                'data': {
                    'backup_codes': backup_codes
                }
            }), 200
        except Exception as e:
            session.rollback()
            logger.error(f"Error regenerating backup codes: {str(e)}")
            
            return jsonify({
                'status': 'error',
                'message': 'Error regenerating backup codes'
            }), 500
        finally:
            session.close()
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid verification code'
        }), 400

@two_factor_bp.route('/status', methods=['GET'])
@jwt_required()
def get_2fa_status():
    """Get two-factor authentication status."""
    user_id = get_jwt_identity()
    
    # Get user from database
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': {
            'enabled': user.otp_enabled,
            'verified': user.otp_verified,
            'has_backup_codes': bool(user.backup_codes)
        }
    }), 200
