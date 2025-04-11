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
from models.vm import create_vm, get_vm_by_id, get_vm_by_provider_id, get_vms_by_user, update_vm, delete_vm as db_delete_vm

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
    """Get all VMs for the authenticated user."""
    # Get user ID from JWT token
    user_id = get_jwt_identity()

    # Get all VMs for the user from the database
    vms = get_vms_by_user(user_id)

    # Convert VMs to dictionaries
    vm_dicts = [vm.to_dict() for vm in vms]

    return jsonify({
        'status': 'success',
        'data': vm_dicts
    }), 200

@vm_provision_bp.route('/vms', methods=['POST'])
@jwt_required()
def create_vm_endpoint():
    """Create a new VM."""
    data = request.json
    user_id = get_jwt_identity()

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
        # Create VM in cloud provider
        cloud_vm = provider.create_vm(
            name=data['name'],
            region=data['region'],
            size=data.get('size', 'small')
        )

        # Create VM in database
        db_vm = create_vm(
            name=data['name'],
            provider=provider_name,
            region=data['region'],
            instance_type=cloud_vm.get('instance_type', data.get('size', 'small')),
            user_id=user_id,
            vm_id=cloud_vm.get('id'),
            ip_address=cloud_vm.get('ip_address'),
            status=cloud_vm.get('status', 'provisioning')
        )

        if not db_vm:
            return jsonify({
                'status': 'error',
                'message': 'Error creating VM in database'
            }), 500

        return jsonify({
            'status': 'success',
            'message': 'VM created successfully',
            'data': db_vm.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error creating VM: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error creating VM: {str(e)}'
        }), 500

@vm_provision_bp.route('/vms/<int:vm_id>', methods=['GET'])
@jwt_required()
def get_vm_endpoint(vm_id):
    """Get a specific VM by ID."""
    user_id = get_jwt_identity()

    # Get VM from database
    vm = get_vm_by_id(vm_id)

    if not vm:
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {vm_id} not found'
        }), 404

    # Check if the VM belongs to the authenticated user
    if vm.user_id != user_id:
        return jsonify({
            'status': 'error',
            'message': 'You do not have permission to access this VM'
        }), 403

    # Get provider instance
    provider = get_provider_instance(vm.provider)

    # Get VM details from cloud provider if available
    if vm.vm_id:
        try:
            cloud_vm = provider.get_vm(vm.vm_id)
            if cloud_vm and cloud_vm.get('status') != vm.status:
                # Update VM status in database if it has changed
                vm = update_vm(vm.id, status=cloud_vm.get('status'))
        except Exception as e:
            logger.warning(f"Error getting VM details from provider: {str(e)}")

    return jsonify({
        'status': 'success',
        'data': vm.to_dict()
    }), 200

@vm_provision_bp.route('/vms/<int:vm_id>', methods=['PUT'])
@jwt_required()
def update_vm_endpoint(vm_id):
    """Update a specific VM by ID."""
    data = request.json
    user_id = get_jwt_identity()

    # Get VM from database
    vm = get_vm_by_id(vm_id)

    if not vm:
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {vm_id} not found'
        }), 404

    # Check if the VM belongs to the authenticated user
    if vm.user_id != user_id:
        return jsonify({
            'status': 'error',
            'message': 'You do not have permission to update this VM'
        }), 403

    # Get provider instance
    provider = get_provider_instance(vm.provider)

    # Update VM in cloud provider if needed
    if vm.vm_id and 'status' in data:
        try:
            # In a real implementation, this would call the provider's API to update the VM
            # For now, we'll just log the action
            logger.info(f"Updating VM {vm.vm_id} in provider {vm.provider} with status {data['status']}")
        except Exception as e:
            logger.error(f"Error updating VM in provider: {str(e)}")

    # Update VM in database
    try:
        # Only allow updating certain fields
        allowed_fields = ['name', 'status']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}

        updated_vm = update_vm(vm.id, **update_data)

        if not updated_vm:
            return jsonify({
                'status': 'error',
                'message': 'Error updating VM in database'
            }), 500

        return jsonify({
            'status': 'success',
            'message': f'VM with ID {vm_id} updated successfully',
            'data': updated_vm.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error updating VM: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error updating VM: {str(e)}'
        }), 500

@vm_provision_bp.route('/vms/<int:vm_id>', methods=['DELETE'])
@jwt_required()
def delete_vm_endpoint(vm_id):
    """Delete a specific VM by ID."""
    user_id = get_jwt_identity()

    # Get VM from database
    vm = get_vm_by_id(vm_id)

    if not vm:
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {vm_id} not found'
        }), 404

    # Check if the VM belongs to the authenticated user
    if vm.user_id != user_id:
        return jsonify({
            'status': 'error',
            'message': 'You do not have permission to delete this VM'
        }), 403

    # Delete VM from cloud provider if it exists
    if vm.vm_id:
        try:
            # Get provider instance
            provider = get_provider_instance(vm.provider)

            # Delete VM from cloud provider
            provider.delete_vm(vm.vm_id)
        except Exception as e:
            logger.error(f"Error deleting VM from provider: {str(e)}")

    # Delete VM from database
    if db_delete_vm(vm.id):
        return jsonify({
            'status': 'success',
            'message': f'VM with ID {vm_id} deleted successfully'
        }), 200

    return jsonify({
        'status': 'error',
        'message': f'Error deleting VM from database'
    }), 500

@vm_provision_bp.route('/vms/<int:vm_id>/start', methods=['POST'])
@jwt_required()
def start_vm_endpoint(vm_id):
    """Start a specific VM by ID."""
    user_id = get_jwt_identity()

    # Get VM from database
    vm = get_vm_by_id(vm_id)

    if not vm:
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {vm_id} not found'
        }), 404

    # Check if the VM belongs to the authenticated user
    if vm.user_id != user_id:
        return jsonify({
            'status': 'error',
            'message': 'You do not have permission to start this VM'
        }), 403

    # Check if VM is already running
    if vm.status == 'running':
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {vm_id} is already running'
        }), 400

    # Start VM in cloud provider if it exists
    if vm.vm_id:
        try:
            # Get provider instance
            provider = get_provider_instance(vm.provider)

            # Start VM in cloud provider
            provider.start_vm(vm.vm_id)
        except Exception as e:
            logger.error(f"Error starting VM in provider: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Error starting VM in provider: {str(e)}'
            }), 500

    # Update VM status in database
    updated_vm = update_vm(vm.id, status='running')

    if updated_vm:
        return jsonify({
            'status': 'success',
            'message': f'VM with ID {vm_id} started successfully',
            'data': updated_vm.to_dict()
        }), 200

    return jsonify({
        'status': 'error',
        'message': f'Error updating VM status in database'
    }), 500

@vm_provision_bp.route('/vms/<int:vm_id>/stop', methods=['POST'])
@jwt_required()
def stop_vm_endpoint(vm_id):
    """Stop a specific VM by ID."""
    user_id = get_jwt_identity()

    # Get VM from database
    vm = get_vm_by_id(vm_id)

    if not vm:
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {vm_id} not found'
        }), 404

    # Check if the VM belongs to the authenticated user
    if vm.user_id != user_id:
        return jsonify({
            'status': 'error',
            'message': 'You do not have permission to stop this VM'
        }), 403

    # Check if VM is already stopped
    if vm.status == 'stopped':
        return jsonify({
            'status': 'error',
            'message': f'VM with ID {vm_id} is already stopped'
        }), 400

    # Stop VM in cloud provider if it exists
    if vm.vm_id:
        try:
            # Get provider instance
            provider = get_provider_instance(vm.provider)

            # Stop VM in cloud provider
            provider.stop_vm(vm.vm_id)
        except Exception as e:
            logger.error(f"Error stopping VM in provider: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Error stopping VM in provider: {str(e)}'
            }), 500

    # Update VM status in database
    updated_vm = update_vm(vm.id, status='stopped')

    if updated_vm:
        return jsonify({
            'status': 'success',
            'message': f'VM with ID {vm_id} stopped successfully',
            'data': updated_vm.to_dict()
        }), 200

    return jsonify({
        'status': 'error',
        'message': f'Error updating VM status in database'
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
