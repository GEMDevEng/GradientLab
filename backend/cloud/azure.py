"""
Azure Cloud provider implementation.
"""
import logging
import requests
import json
import os
from datetime import datetime
from cloud.provider import CloudProvider

logger = logging.getLogger(__name__)

class AzureCloudProvider(CloudProvider):
    """Azure Cloud provider implementation."""
    
    def __init__(self, credentials=None):
        """Initialize Azure Cloud provider."""
        self.credentials = credentials or {}
        self.api_key = self.credentials.get('api_key') or os.environ.get('AZURE_API_KEY')
        self.subscription_id = self.credentials.get('subscription_id') or os.environ.get('AZURE_SUBSCRIPTION_ID')
        self.tenant_id = self.credentials.get('tenant_id') or os.environ.get('AZURE_TENANT_ID')
        self.client_id = self.credentials.get('client_id') or os.environ.get('AZURE_CLIENT_ID')
        self.client_secret = self.credentials.get('client_secret') or os.environ.get('AZURE_CLIENT_SECRET')
        
        # For development/testing, we'll use mock data
        self.mock_vms = []
        self.mock_vm_counter = 0
        
        # Mock regions
        self.regions = [
            {"id": "eastus", "name": "East US", "available": True},
            {"id": "westus", "name": "West US", "available": True},
            {"id": "northeurope", "name": "North Europe", "available": True},
            {"id": "westeurope", "name": "West Europe", "available": True},
            {"id": "eastasia", "name": "East Asia", "available": True}
        ]
    
    def create_vm(self, name, region, size="small"):
        """Create a new VM."""
        logger.info(f"Creating Azure VM: {name} in {region}")
        
        # In a real implementation, this would call the Azure Cloud API
        # For now, we'll create a mock VM
        self.mock_vm_counter += 1
        resource_group = "gradientlab-rg"
        vm_id = f"/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines/{name}-{self.mock_vm_counter}"
        
        # Map size to instance type
        instance_types = {
            "small": "Standard_B1s",
            "medium": "Standard_B2s",
            "large": "Standard_B4ms"
        }
        instance_type = instance_types.get(size, "Standard_B1s")
        
        # Create mock VM
        vm = {
            "id": vm_id,
            "name": name,
            "provider": "azure",
            "region": region,
            "instance_type": instance_type,
            "ip_address": f"40.76.0.{self.mock_vm_counter}",
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
        logger.info(f"Deleting Azure VM: {vm_id}")
        
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
        logger.info(f"Starting Azure VM: {vm_id}")
        
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
        logger.info(f"Stopping Azure VM: {vm_id}")
        
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
        logger.info(f"Getting Azure VM details: {vm_id}")
        
        # Find the VM in our mock data
        for vm in self.mock_vms:
            if vm["id"] == vm_id:
                return vm
        
        # VM not found
        logger.error(f"VM not found: {vm_id}")
        return None
    
    def list_vms(self):
        """List all VMs."""
        logger.info("Listing Azure VMs")
        return self.mock_vms
    
    def list_regions(self):
        """List available regions."""
        logger.info("Listing Azure regions")
        return self.regions
