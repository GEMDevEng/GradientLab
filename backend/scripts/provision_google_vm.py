#!/usr/bin/env python3
"""
Script to provision a VM on Google Cloud Platform (GCP) using the Google Cloud SDK.
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
    from google.cloud import compute_v1
    from google.auth import default
except ImportError:
    print("Google Cloud SDK not installed. Installing...")
    os.system("pip install google-cloud-compute google-auth")
    from google.cloud import compute_v1
    from google.auth import default

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("google_vm_provision.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_credentials():
    """Get Google Cloud credentials."""
    try:
        credentials, project = default()
        return credentials, project
    except Exception as e:
        logger.error(f"Error getting Google Cloud credentials: {str(e)}")
        sys.exit(1)

def create_instance(project_id, zone, instance_name, machine_type="e2-micro", image_family="ubuntu-2004-lts", image_project="ubuntu-os-cloud"):
    """Create a compute instance on Google Cloud Platform."""
    try:
        # Initialize the Compute Engine client
        instance_client = compute_v1.InstancesClient()
        
        # Get the latest image
        image_client = compute_v1.ImagesClient()
        image_response = image_client.get_from_family(
            project=image_project,
            family=image_family
        )
        source_disk_image = image_response.self_link
        
        # Configure the machine
        machine_type_full = f"zones/{zone}/machineTypes/{machine_type}"
        
        # Configure the network interface
        network_interface = compute_v1.NetworkInterface()
        network_interface.name = "global/networks/default"
        access_config = compute_v1.AccessConfig()
        access_config.name = "External NAT"
        access_config.type_ = "ONE_TO_ONE_NAT"
        access_config.network_tier = "PREMIUM"
        network_interface.access_configs = [access_config]
        
        # Configure the boot disk
        disk = compute_v1.AttachedDisk()
        disk.boot = True
        disk.auto_delete = True
        initialize_params = compute_v1.AttachedDiskInitializeParams()
        initialize_params.source_image = source_disk_image
        initialize_params.disk_size_gb = 10
        initialize_params.disk_type = f"zones/{zone}/diskTypes/pd-standard"
        disk.initialize_params = initialize_params
        
        # Configure SSH keys if provided
        metadata = compute_v1.Metadata()
        ssh_key = os.environ.get("GCP_SSH_PUBLIC_KEY")
        if ssh_key:
            metadata.items = [
                compute_v1.Items(
                    key="ssh-keys",
                    value=f"ubuntu:{ssh_key}"
                )
            ]
        
        # Create the instance
        instance = compute_v1.Instance()
        instance.name = instance_name
        instance.machine_type = machine_type_full
        instance.disks = [disk]
        instance.network_interfaces = [network_interface]
        instance.metadata = metadata
        
        # Create a request to insert an instance
        request = compute_v1.InsertInstanceRequest()
        request.zone = zone
        request.project = project_id
        request.instance_resource = instance
        
        # Make the request
        operation = instance_client.insert(request=request)
        
        # Wait for the operation to complete
        while operation.status != compute_v1.Operation.Status.DONE:
            operation = instance_client.get_operation(
                project=project_id,
                zone=zone,
                operation=operation.name
            )
            time.sleep(1)
        
        if operation.error:
            logger.error(f"Error creating instance: {operation.error.errors}")
            sys.exit(1)
        
        # Get the created instance
        instance = instance_client.get(
            project=project_id,
            zone=zone,
            instance=instance_name
        )
        
        logger.info(f"Instance created: {instance.name}")
        return instance
    except Exception as e:
        logger.error(f"Error creating instance: {str(e)}")
        sys.exit(1)

def get_instance_ip(instance):
    """Get the public IP address of the instance."""
    try:
        for network_interface in instance.network_interfaces:
            for access_config in network_interface.access_configs:
                if access_config.nat_i_p:
                    logger.info(f"Instance public IP: {access_config.nat_i_p}")
                    return access_config.nat_i_p
        
        logger.error("No public IP found for instance")
        return None
    except Exception as e:
        logger.error(f"Error getting instance IP: {str(e)}")
        return None

def provision_vm(project_id=None, zone="us-central1-a", instance_name=None, machine_type="e2-micro"):
    """Provision a VM on Google Cloud Platform."""
    start_time = datetime.now()
    logger.info(f"Starting VM provisioning at {start_time}")
    
    # Get credentials
    credentials, default_project = get_credentials()
    
    # Use default project if not provided
    if not project_id:
        project_id = default_project
        if not project_id:
            logger.error("Project ID not provided and not found in credentials")
            sys.exit(1)
    
    # Use default instance name if not provided
    if not instance_name:
        instance_name = f"gradientlab-vm-{int(time.time())}"
    
    # Create instance
    instance = create_instance(
        project_id=project_id,
        zone=zone,
        instance_name=instance_name,
        machine_type=machine_type
    )
    
    # Get instance IP
    ip_address = get_instance_ip(instance)
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"VM provisioning completed at {end_time} (duration: {duration})")
    
    # Return VM details
    vm_details = {
        "id": instance.id,
        "name": instance.name,
        "project_id": project_id,
        "zone": zone,
        "machine_type": instance.machine_type,
        "status": instance.status,
        "creation_timestamp": instance.creation_timestamp,
        "ip_address": ip_address
    }
    
    logger.info(f"VM details: {json.dumps(vm_details, indent=2)}")
    return vm_details

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provision a VM on Google Cloud Platform")
    parser.add_argument("--project-id", help="Google Cloud Project ID")
    parser.add_argument("--zone", default="us-central1-a", help="Google Cloud Zone")
    parser.add_argument("--instance-name", help="Name for the VM instance")
    parser.add_argument("--machine-type", default="e2-micro", help="Machine type for the VM")
    args = parser.parse_args()
    
    vm_details = provision_vm(args.project_id, args.zone, args.instance_name, args.machine_type)
    print(json.dumps(vm_details, indent=2))
