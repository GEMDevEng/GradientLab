"""
Real-time API for GradientLab backend.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from datetime import datetime

from models.node import get_node_by_id, update_node
from models.vm import get_vm_by_id
from websocket.socket_manager import broadcast_node_status_update, broadcast_reward_update

logger = logging.getLogger(__name__)

# Create blueprint
realtime_bp = Blueprint('realtime', __name__)

@realtime_bp.route('/node/<int:node_id>/status', methods=['POST'])
@jwt_required()
def update_node_status(node_id):
    """Update node status and broadcast to subscribed clients."""
    user_id = get_jwt_identity()
    data = request.json
    
    # Validate required fields
    required_fields = ['status', 'uptime_percentage']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Get node from database
    node = get_node_by_id(node_id)
    if not node:
        return jsonify({
            'status': 'error',
            'message': f'Node with ID {node_id} not found'
        }), 404
    
    # Get VM to check ownership
    vm = get_vm_by_id(node.vm_id)
    if not vm:
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {node.vm_id} not found'
        }), 404
    
    # Check if the VM belongs to the authenticated user
    if vm.user_id != user_id:
        return jsonify({
            'status': 'error',
            'message': 'You do not have permission to update this node'
        }), 403
    
    # Update node in database
    update_data = {
        'status': data['status'],
        'uptime_percentage': data['uptime_percentage']
    }
    
    updated_node = update_node(node_id, **update_data)
    if not updated_node:
        return jsonify({
            'status': 'error',
            'message': 'Error updating node in database'
        }), 500
    
    # Prepare data for WebSocket broadcast
    status_data = {
        'node_id': node_id,
        'status': data['status'],
        'uptime_percentage': data['uptime_percentage'],
        'updated_at': datetime.utcnow().isoformat()
    }
    
    # Broadcast to subscribed clients
    broadcast_node_status_update(node_id, status_data)
    
    return jsonify({
        'status': 'success',
        'message': f'Node status updated and broadcasted',
        'data': updated_node.to_dict()
    }), 200

@realtime_bp.route('/reward/update', methods=['POST'])
@jwt_required()
def update_reward():
    """Update reward and broadcast to user."""
    user_id = get_jwt_identity()
    data = request.json
    
    # Validate required fields
    required_fields = ['node_id', 'poa_points', 'poc_points', 'referral_points']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Get node from database
    node = get_node_by_id(data['node_id'])
    if not node:
        return jsonify({
            'status': 'error',
            'message': f'Node with ID {data["node_id"]} not found'
        }), 404
    
    # Get VM to check ownership
    vm = get_vm_by_id(node.vm_id)
    if not vm:
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {node.vm_id} not found'
        }), 404
    
    # Check if the VM belongs to the authenticated user
    if vm.user_id != user_id:
        return jsonify({
            'status': 'error',
            'message': 'You do not have permission to update rewards for this node'
        }), 403
    
    # Prepare data for WebSocket broadcast
    reward_data = {
        'node_id': data['node_id'],
        'poa_points': data['poa_points'],
        'poc_points': data['poc_points'],
        'referral_points': data['referral_points'],
        'total_points': data['poa_points'] + data['poc_points'] + data['referral_points'],
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Broadcast to user
    broadcast_reward_update(user_id, reward_data)
    
    return jsonify({
        'status': 'success',
        'message': 'Reward update broadcasted',
        'data': reward_data
    }), 200

@realtime_bp.route('/status', methods=['GET'])
def get_realtime_status():
    """Get real-time system status."""
    from websocket.socket_manager import get_connected_clients_count, get_authenticated_clients_count
    
    return jsonify({
        'status': 'success',
        'data': {
            'connected_clients': get_connected_clients_count(),
            'authenticated_clients': get_authenticated_clients_count(),
            'server_time': datetime.utcnow().isoformat()
        }
    }), 200
