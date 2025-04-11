"""
Referral Management API endpoints.
This module handles the management of referral relationships between nodes.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime

# Create a Blueprint for referral management
referral_manage_bp = Blueprint('referral_manage', __name__)

# Mock data for development (will be replaced with actual database)
mock_referrals = []

@referral_manage_bp.route('/referrals', methods=['GET'])
def get_referrals():
    """Get all referrals."""
    return jsonify({
        'status': 'success',
        'data': mock_referrals
    }), 200

@referral_manage_bp.route('/referrals/node/<int:node_id>', methods=['GET'])
def get_node_referrals(node_id):
    """Get referrals for a specific node (both as referrer and referred)."""
    # Get referrals where the node is the referrer
    referrer_referrals = [referral for referral in mock_referrals if referral['referrer_node_id'] == node_id]
    
    # Get referrals where the node is the referred
    referred_referrals = [referral for referral in mock_referrals if referral['referred_node_id'] == node_id]
    
    return jsonify({
        'status': 'success',
        'data': {
            'as_referrer': referrer_referrals,
            'as_referred': referred_referrals
        }
    }), 200

@referral_manage_bp.route('/referrals', methods=['POST'])
def create_referral():
    """Create a new referral relationship."""
    data = request.json
    
    # Validate required fields
    required_fields = ['referrer_node_id', 'referred_node_id']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Check if the referral already exists
    for referral in mock_referrals:
        if (referral['referrer_node_id'] == data['referrer_node_id'] and 
            referral['referred_node_id'] == data['referred_node_id']):
            return jsonify({
                'status': 'error',
                'message': 'This referral relationship already exists'
            }), 400
    
    # Check if the node is trying to refer itself
    if data['referrer_node_id'] == data['referred_node_id']:
        return jsonify({
            'status': 'error',
            'message': 'A node cannot refer itself'
        }), 400
    
    # Create a new referral (mock implementation)
    new_referral = {
        'id': len(mock_referrals) + 1,
        'referrer_node_id': data['referrer_node_id'],
        'referred_node_id': data['referred_node_id'],
        'bonus_percentage': data.get('bonus_percentage', 10.0),  # Default to 10% bonus
        'created_at': datetime.now().isoformat()
    }
    
    mock_referrals.append(new_referral)
    
    return jsonify({
        'status': 'success',
        'message': 'Referral created successfully',
        'data': new_referral
    }), 201

@referral_manage_bp.route('/referrals/<int:referral_id>', methods=['DELETE'])
def delete_referral(referral_id):
    """Delete a specific referral by ID."""
    for i, referral in enumerate(mock_referrals):
        if referral['id'] == referral_id:
            deleted_referral = mock_referrals.pop(i)
            
            return jsonify({
                'status': 'success',
                'message': f'Referral with ID {referral_id} deleted successfully',
                'data': deleted_referral
            }), 200
    
    return jsonify({
        'status': 'error',
        'message': f'Referral with ID {referral_id} not found'
    }), 404

@referral_manage_bp.route('/referrals/stats', methods=['GET'])
def get_referral_stats():
    """Get aggregated referral statistics."""
    if not mock_referrals:
        return jsonify({
            'status': 'success',
            'data': {
                'total_referrals': 0,
                'unique_referrers': 0,
                'unique_referred': 0,
                'average_bonus_percentage': 0
            }
        }), 200
    
    # Calculate statistics
    total_referrals = len(mock_referrals)
    
    # Get unique referrer and referred node IDs
    unique_referrers = set(referral['referrer_node_id'] for referral in mock_referrals)
    unique_referred = set(referral['referred_node_id'] for referral in mock_referrals)
    
    # Calculate average bonus percentage
    total_bonus_percentage = sum(referral['bonus_percentage'] for referral in mock_referrals)
    average_bonus_percentage = total_bonus_percentage / total_referrals
    
    return jsonify({
        'status': 'success',
        'data': {
            'total_referrals': total_referrals,
            'unique_referrers': len(unique_referrers),
            'unique_referred': len(unique_referred),
            'average_bonus_percentage': average_bonus_percentage
        }
    }), 200
