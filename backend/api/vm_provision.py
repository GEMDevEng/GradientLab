"""
VM Provisioning API endpoints.
This module handles the creation, management, and deletion of VMs on cloud platforms.
"""
from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime

# Create a Blueprint for VM provisioning
vm_provision_bp = Blueprint('vm_provision', __name__)

# Mock data for development (will be replaced with actual cloud provider APIs)
mock_vms = []

@vm_provision_bp.route('/vms', methods=['GET'])
def get_vms():
    """Get all VMs."""
    return jsonify({
        'status': 'success',
        'data': mock_vms
    }), 200

@vm_provision_bp.route('/vms', methods=['POST'])
def create_vm():
    """Create a new VM."""
    data = request.json
    
    # Validate required fields
    required_fields = ['provider', 'region', 'name']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Create a new VM (mock implementation)
    new_vm = {
        'id': len(mock_vms) + 1,
        'provider': data['provider'],
        'region': data['region'],
        'name': data['name'],
        'ip_address': f'192.168.1.{len(mock_vms) + 1}',  # Mock IP address
        'status': 'provisioning',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    mock_vms.append(new_vm)
    
    return jsonify({
        'status': 'success',
        'message': 'VM created successfully',
        'data': new_vm
    }), 201

@vm_provision_bp.route('/vms/<int:vm_id>', methods=['GET'])
def get_vm(vm_id):
    """Get a specific VM by ID."""
    for vm in mock_vms:
        if vm['id'] == vm_id:
            return jsonify({
                'status': 'success',
                'data': vm
            }), 200
    
    return jsonify({
        'status': 'error',
        'message': f'VM with ID {vm_id} not found'
    }), 404

@vm_provision_bp.route('/vms/<int:vm_id>', methods=['PUT'])
def update_vm(vm_id):
    """Update a specific VM by ID."""
    data = request.json
    
    for i, vm in enumerate(mock_vms):
        if vm['id'] == vm_id:
            # Update VM properties
            for key, value in data.items():
                if key not in ['id', 'created_at']:  # Don't allow updating these fields
                    mock_vms[i][key] = value
            
            mock_vms[i]['updated_at'] = datetime.now().isoformat()
            
            return jsonify({
                'status': 'success',
                'message': f'VM with ID {vm_id} updated successfully',
                'data': mock_vms[i]
            }), 200
    
    return jsonify({
        'status': 'error',
        'message': f'VM with ID {vm_id} not found'
    }), 404

@vm_provision_bp.route('/vms/<int:vm_id>', methods=['DELETE'])
def delete_vm(vm_id):
    """Delete a specific VM by ID."""
    for i, vm in enumerate(mock_vms):
        if vm['id'] == vm_id:
            deleted_vm = mock_vms.pop(i)
            
            return jsonify({
                'status': 'success',
                'message': f'VM with ID {vm_id} deleted successfully',
                'data': deleted_vm
            }), 200
    
    return jsonify({
        'status': 'error',
        'message': f'VM with ID {vm_id} not found'
    }), 404

@vm_provision_bp.route('/vms/<int:vm_id>/start', methods=['POST'])
def start_vm(vm_id):
    """Start a specific VM by ID."""
    for i, vm in enumerate(mock_vms):
        if vm['id'] == vm_id:
            if mock_vms[i]['status'] == 'running':
                return jsonify({
                    'status': 'error',
                    'message': f'VM with ID {vm_id} is already running'
                }), 400
            
            mock_vms[i]['status'] = 'running'
            mock_vms[i]['updated_at'] = datetime.now().isoformat()
            
            return jsonify({
                'status': 'success',
                'message': f'VM with ID {vm_id} started successfully',
                'data': mock_vms[i]
            }), 200
    
    return jsonify({
        'status': 'error',
        'message': f'VM with ID {vm_id} not found'
    }), 404

@vm_provision_bp.route('/vms/<int:vm_id>/stop', methods=['POST'])
def stop_vm(vm_id):
    """Stop a specific VM by ID."""
    for i, vm in enumerate(mock_vms):
        if vm['id'] == vm_id:
            if mock_vms[i]['status'] == 'stopped':
                return jsonify({
                    'status': 'error',
                    'message': f'VM with ID {vm_id} is already stopped'
                }), 400
            
            mock_vms[i]['status'] = 'stopped'
            mock_vms[i]['updated_at'] = datetime.now().isoformat()
            
            return jsonify({
                'status': 'success',
                'message': f'VM with ID {vm_id} stopped successfully',
                'data': mock_vms[i]
            }), 200
    
    return jsonify({
        'status': 'error',
        'message': f'VM with ID {vm_id} not found'
    }), 404

@vm_provision_bp.route('/providers', methods=['GET'])
def get_providers():
    """Get all supported cloud providers."""
    providers = [
        {
            'id': 'oracle',
            'name': 'Oracle Cloud',
            'description': 'Oracle Cloud Infrastructure',
            'free_tier': {
                'vms': 4,
                'ram_per_vm': '6 GB',
                'storage': '200 GB'
            }
        },
        {
            'id': 'google',
            'name': 'Google Cloud Platform',
            'description': 'Google Cloud Platform',
            'free_tier': {
                'vms': 1,
                'ram_per_vm': '0.6 GB',
                'storage': '30 GB'
            }
        },
        {
            'id': 'azure',
            'name': 'Microsoft Azure',
            'description': 'Microsoft Azure',
            'free_tier': {
                'vms': 1,
                'ram_per_vm': '1 GB',
                'storage': 'Varies'
            }
        }
    ]
    
    return jsonify({
        'status': 'success',
        'data': providers
    }), 200
