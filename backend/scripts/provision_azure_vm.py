#!/usr/bin/env python3
"""
Script to provision a VM on Microsoft Azure using the Azure SDK for Python.
This script is designed to work with the free tier resources.
"""
import os
import sys
import time
import json
import logging
import argparse
from datetime import datetime

try:
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.resource import ResourceManagementClient
    from azure.mgmt.network import NetworkManagementClient
    from azure.mgmt.compute import ComputeManagementClient
except ImportError:
    print("Azure SDK not installed. Installing...")
    os.system("pip install azure-identity azure-mgmt-resource azure-mgmt-network azure-mgmt-compute")
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.resource import ResourceManagementClient
    from azure.mgmt.network import NetworkManagementClient
    from azure.mgmt.compute import ComputeManagementClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("azure_vm_provision.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_credentials():
    """Get Azure credentials."""
    try:
        credential = DefaultAzureCredential()
        return credential
    except Exception as e:
        logger.error(f"Error getting Azure credentials: {str(e)}")
        sys.exit(1)

def create_resource_group(resource_client, resource_group_name, location):
    """Create a resource group."""
    try:
        resource_group_params = {"location": location}
        resource_group = resource_client.resource_groups.create_or_update(
            resource_group_name, resource_group_params
        )
        logger.info(f"Resource group created: {resource_group.name}")
        return resource_group
    except Exception as e:
        logger.error(f"Error creating resource group: {str(e)}")
        sys.exit(1)

def create_virtual_network(network_client, resource_group_name, location, vnet_name="GradientLab-VNet", subnet_name="GradientLab-Subnet"):
    """Create a virtual network with a subnet."""
    try:
        # Create VNet
        vnet_params = {
            "location": location,
            "address_space": {
                "address_prefixes": ["10.0.0.0/16"]
            },
            "subnets": [
                {
                    "name": subnet_name,
                    "address_prefix": "10.0.0.0/24"
                }
            ]
        }
        
        vnet_poller = network_client.virtual_networks.begin_create_or_update(
            resource_group_name,
            vnet_name,
            vnet_params
        )
        vnet = vnet_poller.result()
        
        logger.info(f"Virtual network created: {vnet.name}")
        
        # Get subnet
        subnet = network_client.subnets.get(
            resource_group_name,
            vnet_name,
            subnet_name
        )
        
        logger.info(f"Subnet created: {subnet.name}")
        
        return vnet, subnet
    except Exception as e:
        logger.error(f"Error creating virtual network: {str(e)}")
        sys.exit(1)

def create_public_ip_address(network_client, resource_group_name, location, ip_name="GradientLab-IP"):
    """Create a public IP address."""
    try:
        ip_params = {
            "location": location,
            "sku": {
                "name": "Standard"
            },
            "public_ip_allocation_method": "Static",
            "public_ip_address_version": "IPV4"
        }
        
        ip_poller = network_client.public_ip_addresses.begin_create_or_update(
            resource_group_name,
            ip_name,
            ip_params
        )
        ip_address = ip_poller.result()
        
        logger.info(f"Public IP address created: {ip_address.name}")
        return ip_address
    except Exception as e:
        logger.error(f"Error creating public IP address: {str(e)}")
        sys.exit(1)

def create_network_security_group(network_client, resource_group_name, location, nsg_name="GradientLab-NSG"):
    """Create a network security group with required rules."""
    try:
        nsg_params = {
            "location": location,
            "security_rules": [
                {
                    "name": "SSH",
                    "priority": 1000,
                    "protocol": "Tcp",
                    "access": "Allow",
                    "direction": "Inbound",
                    "source_address_prefix": "*",
                    "source_port_range": "*",
                    "destination_address_prefix": "*",
                    "destination_port_range": "22"
                },
                {
                    "name": "HTTP",
                    "priority": 1001,
                    "protocol": "Tcp",
                    "access": "Allow",
                    "direction": "Inbound",
                    "source_address_prefix": "*",
                    "source_port_range": "*",
                    "destination_address_prefix": "*",
                    "destination_port_range": "80"
                },
                {
                    "name": "HTTPS",
                    "priority": 1002,
                    "protocol": "Tcp",
                    "access": "Allow",
                    "direction": "Inbound",
                    "source_address_prefix": "*",
                    "source_port_range": "*",
                    "destination_address_prefix": "*",
                    "destination_port_range": "443"
                }
            ]
        }
        
        nsg_poller = network_client.network_security_groups.begin_create_or_update(
            resource_group_name,
            nsg_name,
            nsg_params
        )
        nsg = nsg_poller.result()
        
        logger.info(f"Network security group created: {nsg.name}")
        return nsg
    except Exception as e:
        logger.error(f"Error creating network security group: {str(e)}")
        sys.exit(1)

def create_network_interface(network_client, resource_group_name, location, subnet_id, public_ip_id, nsg_id, nic_name="GradientLab-NIC"):
    """Create a network interface."""
    try:
        nic_params = {
            "location": location,
            "ip_configurations": [
                {
                    "name": "ipconfig1",
                    "subnet": {
                        "id": subnet_id
                    },
                    "public_ip_address": {
                        "id": public_ip_id
                    }
                }
            ],
            "network_security_group": {
                "id": nsg_id
            }
        }
        
        nic_poller = network_client.network_interfaces.begin_create_or_update(
            resource_group_name,
            nic_name,
            nic_params
        )
        nic = nic_poller.result()
        
        logger.info(f"Network interface created: {nic.name}")
        return nic
    except Exception as e:
        logger.error(f"Error creating network interface: {str(e)}")
        sys.exit(1)

def create_vm(compute_client, resource_group_name, location, nic_id, vm_name="GradientLab-VM", vm_size="Standard_B1s"):
    """Create a virtual machine."""
    try:
        # Get SSH public key
        ssh_key = os.environ.get("AZURE_SSH_PUBLIC_KEY", "")
        
        vm_params = {
            "location": location,
            "hardware_profile": {
                "vm_size": vm_size
            },
            "storage_profile": {
                "image_reference": {
                    "publisher": "Canonical",
                    "offer": "UbuntuServer",
                    "sku": "18.04-LTS",
                    "version": "latest"
                },
                "os_disk": {
                    "create_option": "FromImage",
                    "managed_disk": {
                        "storage_account_type": "Standard_LRS"
                    }
                }
            },
            "os_profile": {
                "computer_name": vm_name,
                "admin_username": "azureuser",
                "linux_configuration": {
                    "disable_password_authentication": True,
                    "ssh": {
                        "public_keys": [
                            {
                                "path": "/home/azureuser/.ssh/authorized_keys",
                                "key_data": ssh_key
                            }
                        ]
                    }
                }
            },
            "network_profile": {
                "network_interfaces": [
                    {
                        "id": nic_id
                    }
                ]
            }
        }
        
        vm_poller = compute_client.virtual_machines.begin_create_or_update(
            resource_group_name,
            vm_name,
            vm_params
        )
        vm = vm_poller.result()
        
        logger.info(f"Virtual machine created: {vm.name}")
        return vm
    except Exception as e:
        logger.error(f"Error creating virtual machine: {str(e)}")
        sys.exit(1)

def get_vm_public_ip(network_client, resource_group_name, ip_name):
    """Get the public IP address of the VM."""
    try:
        ip_address = network_client.public_ip_addresses.get(
            resource_group_name,
            ip_name
        )
        
        logger.info(f"VM public IP: {ip_address.ip_address}")
        return ip_address.ip_address
    except Exception as e:
        logger.error(f"Error getting VM public IP: {str(e)}")
        return None

def provision_vm(subscription_id=None, resource_group_name=None, location="eastus", vm_name=None, vm_size="Standard_B1s"):
    """Provision a VM on Microsoft Azure."""
    start_time = datetime.now()
    logger.info(f"Starting VM provisioning at {start_time}")
    
    # Get credentials
    credential = get_credentials()
    
    # Use subscription ID from environment if not provided
    if not subscription_id:
        subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
        if not subscription_id:
            logger.error("Subscription ID not provided and AZURE_SUBSCRIPTION_ID not set")
            sys.exit(1)
    
    # Use default resource group name if not provided
    if not resource_group_name:
        resource_group_name = f"GradientLab-RG-{int(time.time())}"
    
    # Use default VM name if not provided
    if not vm_name:
        vm_name = f"gradientlab-vm-{int(time.time())}"
    
    # Initialize clients
    resource_client = ResourceManagementClient(credential, subscription_id)
    network_client = NetworkManagementClient(credential, subscription_id)
    compute_client = ComputeManagementClient(credential, subscription_id)
    
    # Create resource group
    resource_group = create_resource_group(resource_client, resource_group_name, location)
    
    # Create virtual network and subnet
    vnet_name = f"{vm_name}-vnet"
    subnet_name = f"{vm_name}-subnet"
    vnet, subnet = create_virtual_network(network_client, resource_group_name, location, vnet_name, subnet_name)
    
    # Create public IP address
    ip_name = f"{vm_name}-ip"
    ip_address_resource = create_public_ip_address(network_client, resource_group_name, location, ip_name)
    
    # Create network security group
    nsg_name = f"{vm_name}-nsg"
    nsg = create_network_security_group(network_client, resource_group_name, location, nsg_name)
    
    # Create network interface
    nic_name = f"{vm_name}-nic"
    nic = create_network_interface(
        network_client,
        resource_group_name,
        location,
        subnet.id,
        ip_address_resource.id,
        nsg.id,
        nic_name
    )
    
    # Create VM
    vm = create_vm(compute_client, resource_group_name, location, nic.id, vm_name, vm_size)
    
    # Get VM public IP
    ip_address = get_vm_public_ip(network_client, resource_group_name, ip_name)
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"VM provisioning completed at {end_time} (duration: {duration})")
    
    # Return VM details
    vm_details = {
        "id": vm.id,
        "name": vm.name,
        "resource_group": resource_group_name,
        "location": location,
        "size": vm_size,
        "provisioning_state": vm.provisioning_state,
        "ip_address": ip_address,
        "vnet_id": vnet.id,
        "subnet_id": subnet.id,
        "nic_id": nic.id
    }
    
    logger.info(f"VM details: {json.dumps(vm_details, indent=2)}")
    return vm_details

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provision a VM on Microsoft Azure")
    parser.add_argument("--subscription-id", help="Azure Subscription ID")
    parser.add_argument("--resource-group", help="Azure Resource Group name")
    parser.add_argument("--location", default="eastus", help="Azure location")
    parser.add_argument("--vm-name", help="Name for the VM")
    parser.add_argument("--vm-size", default="Standard_B1s", help="Size for the VM")
    args = parser.parse_args()
    
    vm_details = provision_vm(args.subscription_id, args.resource_group, args.location, args.vm_name, args.vm_size)
    print(json.dumps(vm_details, indent=2))
