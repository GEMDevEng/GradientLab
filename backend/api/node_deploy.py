"""
Node Deployment API endpoints.
This module handles the deployment and management of Sentry Nodes on VMs.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime

# Create a Blueprint for node deployment
node_deploy_bp = Blueprint('node_deploy', __name__)

# Mock data for development (will be replaced with actual database)
mock_nodes = []

@node_deploy_bp.route('/nodes', methods=['GET'])
def get_nodes():
    """Get all nodes."""
    return jsonify({
        'status': 'success',
        'data': mock_nodes
    }), 200

@node_deploy_bp.route('/nodes', methods=['POST'])
def create_node():
    """Deploy a new node on a VM."""
    data = request.json
    
    # Validate required fields
    required_fields = ['vm_id']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Create a new node (mock implementation)
    new_node = {
        'id': len(mock_nodes) + 1,
        'vm_id': data['vm_id'],
        'status': 'deploying',
        'uptime_percentage': 0.0,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    mock_nodes.append(new_node)
    
    return jsonify({
        'status': 'success',
        'message': 'Node deployed successfully',
        'data': new_node
    }), 201

@node_deploy_bp.route('/nodes/<int:node_id>', methods=['GET'])
def get_node(node_id):
    """Get a specific node by ID."""
    for node in mock_nodes:
        if node['id'] == node_id:
            return jsonify({
                'status': 'success',
                'data': node
            }), 200
    
    return jsonify({
        'status': 'error',
        'message': f'Node with ID {node_id} not found'
    }), 404

@node_deploy_bp.route('/nodes/<int:node_id>', methods=['PUT'])
def update_node(node_id):
    """Update a specific node by ID."""
    data = request.json
    
    for i, node in enumerate(mock_nodes):
        if node['id'] == node_id:
            # Update node properties
            for key, value in data.items():
                if key not in ['id', 'created_at']:  # Don't allow updating these fields
                    mock_nodes[i][key] = value
            
            mock_nodes[i]['updated_at'] = datetime.now().isoformat()
            
            return jsonify({
                'status': 'success',
                'message': f'Node with ID {node_id} updated successfully',
                'data': mock_nodes[i]
            }), 200
    
    return jsonify({
        'status': 'error',
        'message': f'Node with ID {node_id} not found'
    }), 404

@node_deploy_bp.route('/nodes/<int:node_id>', methods=['DELETE'])
def delete_node(node_id):
    """Delete a specific node by ID."""
    for i, node in enumerate(mock_nodes):
        if node['id'] == node_id:
            deleted_node = mock_nodes.pop(i)
            
            return jsonify({
                'status': 'success',
                'message': f'Node with ID {node_id} deleted successfully',
                'data': deleted_node
            }), 200
    
    return jsonify({
        'status': 'error',
        'message': f'Node with ID {node_id} not found'
    }), 404

@node_deploy_bp.route('/nodes/<int:node_id>/start', methods=['POST'])
def start_node(node_id):
    """Start a specific node by ID."""
    for i, node in enumerate(mock_nodes):
        if node['id'] == node_id:
            if mock_nodes[i]['status'] == 'running':
                return jsonify({
                    'status': 'error',
                    'message': f'Node with ID {node_id} is already running'
                }), 400
            
            mock_nodes[i]['status'] = 'running'
            mock_nodes[i]['updated_at'] = datetime.now().isoformat()
            
            return jsonify({
                'status': 'success',
                'message': f'Node with ID {node_id} started successfully',
                'data': mock_nodes[i]
            }), 200
    
    return jsonify({
        'status': 'error',
        'message': f'Node with ID {node_id} not found'
    }), 404

@node_deploy_bp.route('/nodes/<int:node_id>/stop', methods=['POST'])
def stop_node(node_id):
    """Stop a specific node by ID."""
    for i, node in enumerate(mock_nodes):
        if node['id'] == node_id:
            if mock_nodes[i]['status'] == 'stopped':
                return jsonify({
                    'status': 'error',
                    'message': f'Node with ID {node_id} is already stopped'
                }), 400
            
            mock_nodes[i]['status'] = 'stopped'
            mock_nodes[i]['updated_at'] = datetime.now().isoformat()
            
            return jsonify({
                'status': 'success',
                'message': f'Node with ID {node_id} stopped successfully',
                'data': mock_nodes[i]
            }), 200
    
    return jsonify({
        'status': 'error',
        'message': f'Node with ID {node_id} not found'
    }), 404
