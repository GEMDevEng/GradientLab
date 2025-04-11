"""
WebSocket manager for GradientLab backend.
"""
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_jwt_extended import decode_token
from flask import request
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

# Initialize SocketIO
socketio = SocketIO()

# Connected clients
connected_clients = {}

# Node status updates
node_status_updates = {}

def init_app(app):
    """Initialize SocketIO with the Flask app."""
    socketio.init_app(
        app,
        cors_allowed_origins="*",  # In production, specify exact origins
        async_mode='eventlet'
    )
    register_handlers()
    logger.info("WebSocket initialized")
    return socketio

def register_handlers():
    """Register WebSocket event handlers."""
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection."""
        logger.info(f"Client connected: {request.sid}")
        connected_clients[request.sid] = {
            'user_id': None,
            'authenticated': False,
            'connected_at': datetime.utcnow().isoformat()
        }
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection."""
        logger.info(f"Client disconnected: {request.sid}")
        if request.sid in connected_clients:
            # Leave all rooms
            if connected_clients[request.sid].get('user_id'):
                leave_room(f"user_{connected_clients[request.sid]['user_id']}")
            
            # Remove client from connected clients
            del connected_clients[request.sid]
    
    @socketio.on('authenticate')
    def handle_authenticate(data):
        """Handle client authentication."""
        token = data.get('token')
        if not token:
            emit('authentication_error', {'message': 'No token provided'})
            return
        
        try:
            # Decode JWT token
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
            
            # Update client info
            connected_clients[request.sid]['user_id'] = user_id
            connected_clients[request.sid]['authenticated'] = True
            
            # Join user-specific room
            join_room(f"user_{user_id}")
            
            # Send success response
            emit('authenticated', {'user_id': user_id})
            
            logger.info(f"Client authenticated: {request.sid}, user_id: {user_id}")
            
            # Send initial data
            send_initial_data(user_id)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            emit('authentication_error', {'message': 'Invalid token'})
    
    @socketio.on('subscribe_node_updates')
    def handle_subscribe_node_updates(data):
        """Handle subscription to node updates."""
        if not connected_clients.get(request.sid, {}).get('authenticated'):
            emit('error', {'message': 'Not authenticated'})
            return
        
        node_id = data.get('node_id')
        if not node_id:
            emit('error', {'message': 'No node ID provided'})
            return
        
        # Join node-specific room
        join_room(f"node_{node_id}")
        logger.info(f"Client {request.sid} subscribed to node {node_id} updates")
        
        # Send latest node status if available
        if node_id in node_status_updates:
            emit('node_status_update', node_status_updates[node_id])
    
    @socketio.on('unsubscribe_node_updates')
    def handle_unsubscribe_node_updates(data):
        """Handle unsubscription from node updates."""
        node_id = data.get('node_id')
        if not node_id:
            emit('error', {'message': 'No node ID provided'})
            return
        
        # Leave node-specific room
        leave_room(f"node_{node_id}")
        logger.info(f"Client {request.sid} unsubscribed from node {node_id} updates")

def send_initial_data(user_id):
    """Send initial data to authenticated client."""
    # Import here to avoid circular imports
    from models.vm import get_vms_by_user
    from models.node import get_nodes_by_vm
    
    try:
        # Get user's VMs
        vms = get_vms_by_user(user_id)
        
        # Get nodes for each VM
        nodes = []
        for vm in vms:
            vm_nodes = get_nodes_by_vm(vm.id)
            nodes.extend(vm_nodes)
        
        # Convert to dictionaries
        vm_dicts = [vm.to_dict() for vm in vms]
        node_dicts = [node.to_dict() for node in nodes]
        
        # Send data to client
        socketio.emit('initial_data', {
            'vms': vm_dicts,
            'nodes': node_dicts
        }, room=f"user_{user_id}")
        
        logger.info(f"Sent initial data to user {user_id}")
    except Exception as e:
        logger.error(f"Error sending initial data: {str(e)}")

def broadcast_node_status_update(node_id, status_data):
    """Broadcast node status update to subscribed clients."""
    try:
        # Store latest status update
        node_status_updates[node_id] = status_data
        
        # Broadcast to node-specific room
        socketio.emit('node_status_update', status_data, room=f"node_{node_id}")
        
        logger.info(f"Broadcasted status update for node {node_id}")
    except Exception as e:
        logger.error(f"Error broadcasting node status update: {str(e)}")

def broadcast_reward_update(user_id, reward_data):
    """Broadcast reward update to user."""
    try:
        socketio.emit('reward_update', reward_data, room=f"user_{user_id}")
        logger.info(f"Broadcasted reward update to user {user_id}")
    except Exception as e:
        logger.error(f"Error broadcasting reward update: {str(e)}")

def get_connected_clients_count():
    """Get the number of connected clients."""
    return len(connected_clients)

def get_authenticated_clients_count():
    """Get the number of authenticated clients."""
    return sum(1 for client in connected_clients.values() if client.get('authenticated'))

def get_client_info(client_id):
    """Get information about a specific client."""
    return connected_clients.get(client_id)
