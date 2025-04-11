"""
VM Provisioning API endpoints.
This module handles the creation, management, and deletion of VMs on cloud platforms.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import os
import logging
from datetime import datetime
from cloud.provider import get_provider
from models.user import get_user_by_id

# Create a Blueprint for VM provisioning
vm_provision_bp = Blueprint('vm_provision', __name__)
logger = logging.getLogger(__name__)

# Initialize cloud providers
providers = {
    'oracle': None,
    'google': None,
    'azure': None
}

def get_provider_instance(provider_name):
    """Get or initialize a cloud provider instance."""
    global providers
    if providers[provider_name] is None:
        providers[provider_name] = get_provider(provider_name)
    return providers[provider_name]

@vm_provision_bp.route('/vms', methods=['GET'])
@jwt_required()
def get_vms():
    """Get all VMs."""
    # Get all VMs from all providers
    all_vms = []
    for provider_name in providers:
        provider = get_provider_instance(provider_name)
        all_vms.extend(provider.list_vms())

    return jsonify({
        'status': 'success',
        'data': all_vms
    }), 200

@vm_provision_bp.route('/vms', methods=['POST'])
@jwt_required()
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

    # Validate provider
    provider_name = data['provider']
    if provider_name not in providers:
        return jsonify({
            'status': 'error',
            'message': f'Unsupported provider: {provider_name}'
        }), 400

    # Get provider instance
    provider = get_provider_instance(provider_name)

    # Create VM using provider
    try:
        new_vm = provider.create_vm(
            name=data['name'],
            region=data['region'],
            size=data.get('size', 'small')
        )

        return jsonify({
            'status': 'success',
            'message': 'VM created successfully',
            'data': new_vm
        }), 201
    except Exception as e:
        logger.error(f"Error creating VM: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error creating VM: {str(e)}'
        }), 500

@vm_provision_bp.route('/vms/<string:vm_id>', methods=['GET'])
@jwt_required()
def get_vm(vm_id):
    """Get a specific VM by ID."""
    # Extract provider from VM ID
    provider_name = None
    if vm_id.startswith('ocid1'):
        provider_name = 'oracle'
    elif 'projects' in vm_id and 'zones' in vm_id and 'instances' in vm_id:
        provider_name = 'google'
    elif 'subscriptions' in vm_id and 'resourceGroups' in vm_id:
        provider_name = 'azure'

    if not provider_name:
        return jsonify({
            'status': 'error',
            'message': f'Unable to determine provider for VM ID: {vm_id}'
        }), 400

    # Get provider instance
    provider = get_provider_instance(provider_name)

    # Get VM details
    vm = provider.get_vm(vm_id)

    if vm:
        return jsonify({
            'status': 'success',
            'data': vm
        }), 200

    return jsonify({
        'status': 'error',
        'message': f'VM with ID {vm_id} not found'
    }), 404

@vm_provision_bp.route('/vms/<string:vm_id>', methods=['PUT'])
@jwt_required()
def update_vm(vm_id):
    """Update a specific VM by ID."""
    data = request.json

    # Extract provider from VM ID
    provider_name = None
    if vm_id.startswith('ocid1'):
        provider_name = 'oracle'
    elif 'projects' in vm_id and 'zones' in vm_id and 'instances' in vm_id:
        provider_name = 'google'
    elif 'subscriptions' in vm_id and 'resourceGroups' in vm_id:
        provider_name = 'azure'

    if not provider_name:
        return jsonify({
            'status': 'error',
            'message': f'Unable to determine provider for VM ID: {vm_id}'
        }), 400

    # Get provider instance
    provider = get_provider_instance(provider_name)

    # Get VM details
    vm = provider.get_vm(vm_id)

    if not vm:
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {vm_id} not found'
        }), 404

    # Update VM properties
    # In a real implementation, this would call the provider's API to update the VM
    # For now, we'll just update our mock data
    for key, value in data.items():
        if key not in ['id', 'provider', 'created_at']:  # Don't allow updating these fields
            vm[key] = value

    vm['updated_at'] = datetime.now().isoformat()

    return jsonify({
        'status': 'success',
        'message': f'VM with ID {vm_id} updated successfully',
        'data': vm
    }), 200

@vm_provision_bp.route('/vms/<string:vm_id>', methods=['DELETE'])
@jwt_required()
def delete_vm(vm_id):
    """Delete a specific VM by ID."""
    # Extract provider from VM ID
    provider_name = None
    if vm_id.startswith('ocid1'):
        provider_name = 'oracle'
    elif 'projects' in vm_id and 'zones' in vm_id and 'instances' in vm_id:
        provider_name = 'google'
    elif 'subscriptions' in vm_id and 'resourceGroups' in vm_id:
        provider_name = 'azure'

    if not provider_name:
        return jsonify({
            'status': 'error',
            'message': f'Unable to determine provider for VM ID: {vm_id}'
        }), 400

    # Get provider instance
    provider = get_provider_instance(provider_name)

    # Delete VM
    deleted_vm = provider.delete_vm(vm_id)

    if deleted_vm:
        return jsonify({
            'status': 'success',
            'message': f'VM with ID {vm_id} deleted successfully',
            'data': deleted_vm
        }), 200

    return jsonify({
        'status': 'error',
        'message': f'VM with ID {vm_id} not found'
    }), 404

@vm_provision_bp.route('/vms/<string:vm_id>/start', methods=['POST'])
@jwt_required()
def start_vm(vm_id):
    """Start a specific VM by ID."""
    # Extract provider from VM ID
    provider_name = None
    if vm_id.startswith('ocid1'):
        provider_name = 'oracle'
    elif 'projects' in vm_id and 'zones' in vm_id and 'instances' in vm_id:
        provider_name = 'google'
    elif 'subscriptions' in vm_id and 'resourceGroups' in vm_id:
        provider_name = 'azure'

    if not provider_name:
        return jsonify({
            'status': 'error',
            'message': f'Unable to determine provider for VM ID: {vm_id}'
        }), 400

    # Get provider instance
    provider = get_provider_instance(provider_name)

    # Get VM details
    vm = provider.get_vm(vm_id)

    if not vm:
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {vm_id} not found'
        }), 404

    # Check if VM is already running
    if vm['status'] == 'running':
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {vm_id} is already running'
        }), 400

    # Start VM
    started_vm = provider.start_vm(vm_id)

    if started_vm:
        return jsonify({
            'status': 'success',
            'message': f'VM with ID {vm_id} started successfully',
            'data': started_vm
        }), 200

    return jsonify({
        'status': 'error',
        'message': f'Failed to start VM with ID {vm_id}'
    }), 500

@vm_provision_bp.route('/vms/<string:vm_id>/stop', methods=['POST'])
@jwt_required()
def stop_vm(vm_id):
    """Stop a specific VM by ID."""
    # Extract provider from VM ID
    provider_name = None
    if vm_id.startswith('ocid1'):
        provider_name = 'oracle'
    elif 'projects' in vm_id and 'zones' in vm_id and 'instances' in vm_id:
        provider_name = 'google'
    elif 'subscriptions' in vm_id and 'resourceGroups' in vm_id:
        provider_name = 'azure'

    if not provider_name:
        return jsonify({
            'status': 'error',
            'message': f'Unable to determine provider for VM ID: {vm_id}'
        }), 400

    # Get provider instance
    provider = get_provider_instance(provider_name)

    # Get VM details
    vm = provider.get_vm(vm_id)

    if not vm:
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {vm_id} not found'
        }), 404

    # Check if VM is already stopped
    if vm['status'] == 'stopped':
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {vm_id} is already stopped'
        }), 400

    # Stop VM
    stopped_vm = provider.stop_vm(vm_id)

    if stopped_vm:
        return jsonify({
            'status': 'success',
            'message': f'VM with ID {vm_id} stopped successfully',
            'data': stopped_vm
        }), 200

    return jsonify({
        'status': 'error',
        'message': f'Failed to stop VM with ID {vm_id}'
    }), 500

@vm_provision_bp.route('/providers', methods=['GET'])
@jwt_required()
def get_providers():
    """Get all supported cloud providers."""
    cloud_providers = [
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

    # Add regions for each provider
    for provider_info in cloud_providers:
        provider_id = provider_info['id']
        provider = get_provider_instance(provider_id)
        provider_info['regions'] = provider.list_regions()

    return jsonify({
        'status': 'success',
        'data': cloud_providers
    }), 200
