"""
Google Cloud provider implementation.
"""
import logging
import requests
import json
import os
from datetime import datetime
from cloud.provider import CloudProvider

logger = logging.getLogger(__name__)

class GoogleCloudProvider(CloudProvider):
    """Google Cloud provider implementation."""
    
    def __init__(self, credentials=None):
        """Initialize Google Cloud provider."""
        self.credentials = credentials or {}
        self.api_key = self.credentials.get('api_key') or os.environ.get('GOOGLE_API_KEY')
        self.project_id = self.credentials.get('project_id') or os.environ.get('GOOGLE_PROJECT_ID')
        
        # For development/testing, we'll use mock data
        self.mock_vms = []
        self.mock_vm_counter = 0
        
        # Mock regions
        self.regions = [
            {"id": "us-central1", "name": "Iowa", "available": True},
            {"id": "us-east1", "name": "South Carolina", "available": True},
            {"id": "us-west1", "name": "Oregon", "available": True},
            {"id": "europe-west1", "name": "Belgium", "available": True},
            {"id": "asia-east1", "name": "Taiwan", "available": True}
        ]
    
    def create_vm(self, name, region, size="small"):
        """Create a new VM."""
        logger.info(f"Creating Google VM: {name} in {region}")
        
        # In a real implementation, this would call the Google Cloud API
        # For now, we'll create a mock VM
        self.mock_vm_counter += 1
        vm_id = f"projects/{self.project_id}/zones/{region}-a/instances/{name}-{self.mock_vm_counter}"
        
        # Map size to instance type
        instance_types = {
            "small": "e2-micro",
            "medium": "e2-small",
            "large": "e2-medium"
        }
        instance_type = instance_types.get(size, "e2-micro")
        
        # Create mock VM
        vm = {
            "id": vm_id,
            "name": name,
            "provider": "google",
            "region": region,
            "instance_type": instance_type,
            "ip_address": f"35.192.0.{self.mock_vm_counter}",
            "status": "provisioning",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        self.mock_vms.append(vm)
        
        # Simulate async provisioning
        # In a real implementation, we would return immediately and update the status later
        vm["status"] = "running"
        
        return vm
    
    def delete_vm(self, vm_id):
        """Delete a VM."""
        logger.info(f"Deleting Google VM: {vm_id}")
        
        # Find the VM in our mock data
        for i, vm in enumerate(self.mock_vms):
            if vm["id"] == vm_id:
                # Remove the VM from our mock data
                deleted_vm = self.mock_vms.pop(i)
                return deleted_vm
        
        # VM not found
        logger.error(f"VM not found: {vm_id}")
        return None
    
    def start_vm(self, vm_id):
        """Start a VM."""
        logger.info(f"Starting Google VM: {vm_id}")
        
        # Find the VM in our mock data
        for i, vm in enumerate(self.mock_vms):
            if vm["id"] == vm_id:
                # Update the VM status
                self.mock_vms[i]["status"] = "running"
                self.mock_vms[i]["updated_at"] = datetime.now().isoformat()
                return self.mock_vms[i]
        
        # VM not found
        logger.error(f"VM not found: {vm_id}")
        return None
    
    def stop_vm(self, vm_id):
        """Stop a VM."""
        logger.info(f"Stopping Google VM: {vm_id}")
        
        # Find the VM in our mock data
        for i, vm in enumerate(self.mock_vms):
            if vm["id"] == vm_id:
                # Update the VM status
                self.mock_vms[i]["status"] = "stopped"
                self.mock_vms[i]["updated_at"] = datetime.now().isoformat()
                return self.mock_vms[i]
        
        # VM not found
        logger.error(f"VM not found: {vm_id}")
        return None
    
    def get_vm(self, vm_id):
        """Get VM details."""
        logger.info(f"Getting Google VM details: {vm_id}")
        
        # Find the VM in our mock data
        for vm in self.mock_vms:
            if vm["id"] == vm_id:
                return vm
        
        # VM not found
        logger.error(f"VM not found: {vm_id}")
        return None
    
    def list_vms(self):
        """List all VMs."""
        logger.info("Listing Google VMs")
        return self.mock_vms
    
    def list_regions(self):
        """List available regions."""
        logger.info("Listing Google regions")
        return self.regions
