#!/usr/bin/env python3
"""
Script to provision VMs on all three cloud providers (Oracle, Google, Azure).
This script provisions VMs, sets them up, and installs the Sentry Node extension.
"""
import os
import sys
import json
import time
import logging
import argparse
import subprocess
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("vm_provisioning.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def provision_oracle_vm(config_file=None, compartment_id=None, display_name=None):
    """Provision a VM on Oracle Cloud Infrastructure."""
    try:
        # Path to the Oracle VM provisioning script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "provision_oracle_vm.py")
        
        # Build command
        command = [script_path]
        if config_file:
            command.extend(["--config", config_file])
        if compartment_id:
            command.extend(["--compartment-id", compartment_id])
        if display_name:
            command.extend(["--display-name", display_name])
        
        # Run the script
        logger.info(f"Provisioning Oracle VM: {' '.join(command)}")
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        # Parse the output
        vm_details = json.loads(result.stdout)
        logger.info(f"Oracle VM provisioned: {vm_details['name']} ({vm_details['ip_address']})")
        
        return vm_details
    except Exception as e:
        logger.error(f"Error provisioning Oracle VM: {str(e)}")
        return None

def provision_google_vm(project_id=None, zone="us-central1-a", instance_name=None, machine_type="e2-micro"):
    """Provision a VM on Google Cloud Platform."""
    try:
        # Path to the Google VM provisioning script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "provision_google_vm.py")
        
        # Build command
        command = [script_path]
        if project_id:
            command.extend(["--project-id", project_id])
        if zone:
            command.extend(["--zone", zone])
        if instance_name:
            command.extend(["--instance-name", instance_name])
        if machine_type:
            command.extend(["--machine-type", machine_type])
        
        # Run the script
        logger.info(f"Provisioning Google VM: {' '.join(command)}")
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        # Parse the output
        vm_details = json.loads(result.stdout)
        logger.info(f"Google VM provisioned: {vm_details['name']} ({vm_details['ip_address']})")
        
        return vm_details
    except Exception as e:
        logger.error(f"Error provisioning Google VM: {str(e)}")
        return None

def provision_azure_vm(subscription_id=None, resource_group=None, location="eastus", vm_name=None, vm_size="Standard_B1s"):
    """Provision a VM on Microsoft Azure."""
    try:
        # Path to the Azure VM provisioning script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "provision_azure_vm.py")
        
        # Build command
        command = [script_path]
        if subscription_id:
            command.extend(["--subscription-id", subscription_id])
        if resource_group:
            command.extend(["--resource-group", resource_group])
        if location:
            command.extend(["--location", location])
        if vm_name:
            command.extend(["--vm-name", vm_name])
        if vm_size:
            command.extend(["--vm-size", vm_size])
        
        # Run the script
        logger.info(f"Provisioning Azure VM: {' '.join(command)}")
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        # Parse the output
        vm_details = json.loads(result.stdout)
        logger.info(f"Azure VM provisioned: {vm_details['name']} ({vm_details['ip_address']})")
        
        return vm_details
    except Exception as e:
        logger.error(f"Error provisioning Azure VM: {str(e)}")
        return None

def install_sentry_node(host, username="ubuntu", key_file=None):
    """Install the Sentry Node extension on a VM."""
    try:
        # Path to the Sentry Node installation script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "install_sentry_node.py")
        
        # Build command
        command = [script_path, host]
        if username:
            command.extend(["--username", username])
        if key_file:
            command.extend(["--key-file", key_file])
        
        # Run the script
        logger.info(f"Installing Sentry Node on {host}: {' '.join(command)}")
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        logger.info(f"Sentry Node installed on {host}")
        return True
    except Exception as e:
        logger.error(f"Error installing Sentry Node on {host}: {str(e)}")
        return False

def save_vm_details(vm_details, nodes_file):
    """Save VM details to the nodes file."""
    try:
        # Load existing nodes
        nodes = []
        if os.path.exists(nodes_file):
            with open(nodes_file, 'r') as f:
                nodes = json.load(f)
        
        # Add new VM
        nodes.append(vm_details)
        
        # Save nodes
        with open(nodes_file, 'w') as f:
            json.dump(nodes, f, indent=2)
        
        logger.info(f"VM details saved to {nodes_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving VM details: {str(e)}")
        return False

def provision_all_vms(nodes_file, num_oracle=1, num_google=1, num_azure=1, key_file=None):
    """Provision VMs on all three cloud providers."""
    start_time = datetime.now()
    logger.info(f"Starting VM provisioning at {start_time}")
    
    # Create nodes file directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(nodes_file)), exist_ok=True)
    
    # Initialize nodes file if it doesn't exist
    if not os.path.exists(nodes_file):
        with open(nodes_file, 'w') as f:
            json.dump([], f)
    
    # Provision Oracle VMs
    for i in range(num_oracle):
        display_name = f"GradientLab-Oracle-{i+1}"
        vm_details = provision_oracle_vm(display_name=display_name)
        
        if vm_details:
            # Add provider and region information
            vm_details['provider'] = 'oracle'
            vm_details['region'] = vm_details.get('availability_domain', '').split(':')[0]
            
            # Save VM details
            save_vm_details(vm_details, nodes_file)
            
            # Install Sentry Node
            install_sentry_node(vm_details['ip_address'], "opc", key_file)
    
    # Provision Google VMs
    for i in range(num_google):
        instance_name = f"gradientlab-google-{i+1}"
        vm_details = provision_google_vm(instance_name=instance_name)
        
        if vm_details:
            # Add provider and region information
            vm_details['provider'] = 'google'
            vm_details['region'] = vm_details.get('zone', '').split('-')[0]
            
            # Save VM details
            save_vm_details(vm_details, nodes_file)
            
            # Install Sentry Node
            install_sentry_node(vm_details['ip_address'], "ubuntu", key_file)
    
    # Provision Azure VMs
    for i in range(num_azure):
        vm_name = f"gradientlab-azure-{i+1}"
        vm_details = provision_azure_vm(vm_name=vm_name)
        
        if vm_details:
            # Add provider and region information
            vm_details['provider'] = 'azure'
            vm_details['region'] = vm_details.get('location', '')
            
            # Save VM details
            save_vm_details(vm_details, nodes_file)
            
            # Install Sentry Node
            install_sentry_node(vm_details['ip_address'], "azureuser", key_file)
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"VM provisioning completed at {end_time} (duration: {duration})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provision VMs on all three cloud providers")
    parser.add_argument("--nodes-file", default="nodes.json", help="Path to nodes JSON file")
    parser.add_argument("--num-oracle", type=int, default=1, help="Number of Oracle VMs to provision")
    parser.add_argument("--num-google", type=int, default=1, help="Number of Google VMs to provision")
    parser.add_argument("--num-azure", type=int, default=1, help="Number of Azure VMs to provision")
    parser.add_argument("--key-file", help="Path to SSH private key file")
    args = parser.parse_args()
    
    provision_all_vms(args.nodes_file, args.num_oracle, args.num_google, args.num_azure, args.key_file)
