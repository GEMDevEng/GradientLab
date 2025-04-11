"""
Cloud provider base class and factory.
"""
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class CloudProvider(ABC):
    """Base class for cloud providers."""
    
    @abstractmethod
    def create_vm(self, name, region, size="small"):
        """Create a new VM."""
        pass
    
    @abstractmethod
    def delete_vm(self, vm_id):
        """Delete a VM."""
        pass
    
    @abstractmethod
    def start_vm(self, vm_id):
        """Start a VM."""
        pass
    
    @abstractmethod
    def stop_vm(self, vm_id):
        """Stop a VM."""
        pass
    
    @abstractmethod
    def get_vm(self, vm_id):
        """Get VM details."""
        pass
    
    @abstractmethod
    def list_vms(self):
        """List all VMs."""
        pass
    
    @abstractmethod
    def list_regions(self):
        """List available regions."""
        pass

def get_provider(provider_name, credentials=None):
    """
    Factory method to get a cloud provider instance.
    
    Args:
        provider_name (str): Name of the provider (oracle, google, azure)
        credentials (dict): Provider-specific credentials
        
    Returns:
        CloudProvider: An instance of the specified cloud provider
    """
    if provider_name == 'oracle':
        from cloud.oracle import OracleCloudProvider
        return OracleCloudProvider(credentials)
    elif provider_name == 'google':
        from cloud.google import GoogleCloudProvider
        return GoogleCloudProvider(credentials)
    elif provider_name == 'azure':
        from cloud.azure import AzureCloudProvider
        return AzureCloudProvider(credentials)
    else:
        logger.error(f"Unsupported provider: {provider_name}")
        raise ValueError(f"Unsupported provider: {provider_name}")
