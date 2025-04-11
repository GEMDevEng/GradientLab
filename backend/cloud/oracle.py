"""
Oracle Cloud provider implementation.
"""
import logging
import requests
import json
import os
from datetime import datetime
from cloud.provider import CloudProvider

logger = logging.getLogger(__name__)

class OracleCloudProvider(CloudProvider):
    """Oracle Cloud provider implementation."""
    
    def __init__(self, credentials=None):
        """Initialize Oracle Cloud provider."""
        self.credentials = credentials or {}
        self.api_key = self.credentials.get('api_key') or os.environ.get('ORACLE_API_KEY')
        self.tenant_id = self.credentials.get('tenant_id') or os.environ.get('ORACLE_TENANT_ID')
        self.user_id = self.credentials.get('user_id') or os.environ.get('ORACLE_USER_ID')
        self.compartment_id = self.credentials.get('compartment_id') or os.environ.get('ORACLE_COMPARTMENT_ID')
        
        # For development/testing, we'll use mock data
        self.mock_vms = []
        self.mock_vm_counter = 0
        
        # Mock regions
        self.regions = [
            {"id": "us-phoenix-1", "name": "Phoenix, AZ", "available": True},
            {"id": "us-ashburn-1", "name": "Ashburn, VA", "available": True},
            {"id": "eu-frankfurt-1", "name": "Frankfurt, Germany", "available": True},
            {"id": "uk-london-1", "name": "London, UK", "available": True},
            {"id": "ap-tokyo-1", "name": "Tokyo, Japan", "available": True}
        ]
    
    def create_vm(self, name, region, size="small"):
        """Create a new VM."""
        logger.info(f"Creating Oracle VM: {name} in {region}")
        
        # In a real implementation, this would call the Oracle Cloud API
        # For now, we'll create a mock VM
        self.mock_vm_counter += 1
        vm_id = f"ocid1.instance.oc1..aaaaaaaa{self.mock_vm_counter}"
        
        # Map size to instance type
        instance_types = {
            "small": "VM.Standard.E2.1",
            "medium": "VM.Standard.E2.2",
            "large": "VM.Standard.E2.4"
        }
        instance_type = instance_types.get(size, "VM.Standard.E2.1")
        
        # Create mock VM
        vm = {
            "id": vm_id,
            "name": name,
            "provider": "oracle",
            "region": region,
            "instance_type": instance_type,
            "ip_address": f"192.168.1.{self.mock_vm_counter}",
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
        logger.info(f"Deleting Oracle VM: {vm_id}")
        
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
        logger.info(f"Starting Oracle VM: {vm_id}")
        
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
        logger.info(f"Stopping Oracle VM: {vm_id}")
        
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
        logger.info(f"Getting Oracle VM details: {vm_id}")
        
        # Find the VM in our mock data
        for vm in self.mock_vms:
            if vm["id"] == vm_id:
                return vm
        
        # VM not found
        logger.error(f"VM not found: {vm_id}")
        return None
    
    def list_vms(self):
        """List all VMs."""
        logger.info("Listing Oracle VMs")
        return self.mock_vms
    
    def list_regions(self):
        """List available regions."""
        logger.info("Listing Oracle regions")
        return self.regions
