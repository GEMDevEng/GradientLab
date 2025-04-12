#!/usr/bin/env python3
"""
Script to provision a VM on Oracle Cloud Infrastructure (OCI) using the OCI Python SDK.
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
    import oci
    from oci.core import ComputeClient, VirtualNetworkClient
    from oci.identity import IdentityClient
except ImportError:
    print("OCI SDK not installed. Installing...")
    os.system("pip install oci")
    import oci
    from oci.core import ComputeClient, VirtualNetworkClient
    from oci.identity import IdentityClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("oracle_vm_provision.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config(config_file=None):
    """Load OCI configuration from file or environment variables."""
    if config_file and os.path.exists(config_file):
        logger.info(f"Loading config from file: {config_file}")
        return oci.config.from_file(config_file)
    
    # Try to load from environment variables
    logger.info("Loading config from environment variables")
    config = {
        "user": os.environ.get("OCI_USER_OCID"),
        "fingerprint": os.environ.get("OCI_FINGERPRINT"),
        "tenancy": os.environ.get("OCI_TENANCY_OCID"),
        "region": os.environ.get("OCI_REGION"),
        "key_file": os.environ.get("OCI_KEY_FILE")
    }
    
    # Check if all required config values are present
    missing_keys = [k for k, v in config.items() if not v]
    if missing_keys:
        logger.error(f"Missing required OCI configuration: {', '.join(missing_keys)}")
        sys.exit(1)
    
    return config

def get_availability_domains(identity_client, compartment_id):
    """Get a list of availability domains."""
    try:
        response = identity_client.list_availability_domains(compartment_id=compartment_id)
        return response.data
    except Exception as e:
        logger.error(f"Error getting availability domains: {str(e)}")
        sys.exit(1)

def create_vcn(virtual_network_client, compartment_id, display_name="GradientLab-VCN"):
    """Create a Virtual Cloud Network (VCN)."""
    try:
        vcn_details = oci.core.models.CreateVcnDetails(
            cidr_block="10.0.0.0/16",
            display_name=display_name,
            compartment_id=compartment_id,
            dns_label="gradientlab"
        )
        response = virtual_network_client.create_vcn(vcn_details)
        logger.info(f"VCN created: {response.data.id}")
        
        # Wait for VCN to be available
        get_vcn_response = oci.wait_until(
            virtual_network_client,
            virtual_network_client.get_vcn(response.data.id),
            'lifecycle_state',
            'AVAILABLE',
            max_wait_seconds=300
        )
        
        return get_vcn_response.data
    except Exception as e:
        logger.error(f"Error creating VCN: {str(e)}")
        sys.exit(1)

def create_internet_gateway(virtual_network_client, compartment_id, vcn_id, display_name="GradientLab-IG"):
    """Create an Internet Gateway."""
    try:
        ig_details = oci.core.models.CreateInternetGatewayDetails(
            compartment_id=compartment_id,
            vcn_id=vcn_id,
            display_name=display_name,
            is_enabled=True
        )
        response = virtual_network_client.create_internet_gateway(ig_details)
        logger.info(f"Internet Gateway created: {response.data.id}")
        
        # Wait for Internet Gateway to be available
        get_ig_response = oci.wait_until(
            virtual_network_client,
            virtual_network_client.get_internet_gateway(response.data.id),
            'lifecycle_state',
            'AVAILABLE',
            max_wait_seconds=300
        )
        
        return get_ig_response.data
    except Exception as e:
        logger.error(f"Error creating Internet Gateway: {str(e)}")
        sys.exit(1)

def update_route_table(virtual_network_client, compartment_id, vcn_id, ig_id):
    """Update the default route table to use the Internet Gateway."""
    try:
        # Get the default route table
        route_tables = virtual_network_client.list_route_tables(
            compartment_id=compartment_id,
            vcn_id=vcn_id
        ).data
        
        default_route_table = next(rt for rt in route_tables if rt.display_name == "Default Route Table for GradientLab-VCN")
        
        # Update the route table
        route_rule = oci.core.models.RouteRule(
            destination="0.0.0.0/0",
            destination_type="CIDR_BLOCK",
            network_entity_id=ig_id
        )
        
        update_details = oci.core.models.UpdateRouteTableDetails(
            route_rules=[route_rule]
        )
        
        response = virtual_network_client.update_route_table(
            rt_id=default_route_table.id,
            update_route_table_details=update_details
        )
        
        logger.info(f"Route table updated: {response.data.id}")
        return response.data
    except Exception as e:
        logger.error(f"Error updating route table: {str(e)}")
        sys.exit(1)

def create_subnet(virtual_network_client, compartment_id, vcn_id, availability_domain, display_name="GradientLab-Subnet"):
    """Create a subnet in the VCN."""
    try:
        subnet_details = oci.core.models.CreateSubnetDetails(
            compartment_id=compartment_id,
            vcn_id=vcn_id,
            availability_domain=availability_domain.name,
            display_name=display_name,
            cidr_block="10.0.0.0/24",
            dns_label="gradientlab"
        )
        
        response = virtual_network_client.create_subnet(subnet_details)
        logger.info(f"Subnet created: {response.data.id}")
        
        # Wait for subnet to be available
        get_subnet_response = oci.wait_until(
            virtual_network_client,
            virtual_network_client.get_subnet(response.data.id),
            'lifecycle_state',
            'AVAILABLE',
            max_wait_seconds=300
        )
        
        return get_subnet_response.data
    except Exception as e:
        logger.error(f"Error creating subnet: {str(e)}")
        sys.exit(1)

def create_security_list(virtual_network_client, compartment_id, vcn_id, display_name="GradientLab-SecurityList"):
    """Create a security list with required ingress and egress rules."""
    try:
        # Allow SSH (port 22), HTTP (port 80), HTTPS (port 443) ingress
        ingress_rules = [
            oci.core.models.IngressSecurityRule(
                protocol="6",  # TCP
                source="0.0.0.0/0",
                source_type="CIDR_BLOCK",
                tcp_options=oci.core.models.TcpOptions(
                    destination_port_range=oci.core.models.PortRange(
                        min=22,
                        max=22
                    )
                )
            ),
            oci.core.models.IngressSecurityRule(
                protocol="6",  # TCP
                source="0.0.0.0/0",
                source_type="CIDR_BLOCK",
                tcp_options=oci.core.models.TcpOptions(
                    destination_port_range=oci.core.models.PortRange(
                        min=80,
                        max=80
                    )
                )
            ),
            oci.core.models.IngressSecurityRule(
                protocol="6",  # TCP
                source="0.0.0.0/0",
                source_type="CIDR_BLOCK",
                tcp_options=oci.core.models.TcpOptions(
                    destination_port_range=oci.core.models.PortRange(
                        min=443,
                        max=443
                    )
                )
            )
        ]
        
        # Allow all egress
        egress_rules = [
            oci.core.models.EgressSecurityRule(
                protocol="all",
                destination="0.0.0.0/0",
                destination_type="CIDR_BLOCK"
            )
        ]
        
        security_list_details = oci.core.models.CreateSecurityListDetails(
            compartment_id=compartment_id,
            vcn_id=vcn_id,
            display_name=display_name,
            ingress_security_rules=ingress_rules,
            egress_security_rules=egress_rules
        )
        
        response = virtual_network_client.create_security_list(security_list_details)
        logger.info(f"Security list created: {response.data.id}")
        
        # Wait for security list to be available
        get_sl_response = oci.wait_until(
            virtual_network_client,
            virtual_network_client.get_security_list(response.data.id),
            'lifecycle_state',
            'AVAILABLE',
            max_wait_seconds=300
        )
        
        return get_sl_response.data
    except Exception as e:
        logger.error(f"Error creating security list: {str(e)}")
        sys.exit(1)

def get_image(compute_client, compartment_id, operating_system="Oracle Linux", os_version="8"):
    """Get the latest Oracle Linux image."""
    try:
        images = compute_client.list_images(
            compartment_id=compartment_id,
            operating_system=operating_system,
            operating_system_version=os_version,
            sort_by="TIMECREATED",
            sort_order="DESC"
        ).data
        
        if not images:
            logger.error(f"No {operating_system} {os_version} images found")
            sys.exit(1)
        
        logger.info(f"Using image: {images[0].id} ({images[0].display_name})")
        return images[0]
    except Exception as e:
        logger.error(f"Error getting image: {str(e)}")
        sys.exit(1)

def create_instance(compute_client, compartment_id, availability_domain, subnet_id, image_id, shape="VM.Standard.E2.1.Micro", display_name="GradientLab-VM"):
    """Create a compute instance."""
    try:
        instance_details = oci.core.models.LaunchInstanceDetails(
            availability_domain=availability_domain.name,
            compartment_id=compartment_id,
            display_name=display_name,
            image_id=image_id,
            shape=shape,
            create_vnic_details=oci.core.models.CreateVnicDetails(
                subnet_id=subnet_id,
                assign_public_ip=True
            ),
            metadata={
                "ssh_authorized_keys": os.environ.get("OCI_SSH_PUBLIC_KEY", "")
            }
        )
        
        response = compute_client.launch_instance(instance_details)
        logger.info(f"Instance creation initiated: {response.data.id}")
        
        # Wait for instance to be running
        get_instance_response = oci.wait_until(
            compute_client,
            compute_client.get_instance(response.data.id),
            'lifecycle_state',
            'RUNNING',
            max_wait_seconds=600
        )
        
        logger.info(f"Instance is running: {get_instance_response.data.id}")
        return get_instance_response.data
    except Exception as e:
        logger.error(f"Error creating instance: {str(e)}")
        sys.exit(1)

def get_instance_ip(compute_client, virtual_network_client, instance_id):
    """Get the public IP address of the instance."""
    try:
        vnic_attachments = compute_client.list_vnic_attachments(
            compartment_id=compute_client.get_instance(instance_id).data.compartment_id,
            instance_id=instance_id
        ).data
        
        if not vnic_attachments:
            logger.error("No VNIC attachments found for instance")
            return None
        
        vnic_id = vnic_attachments[0].vnic_id
        vnic = virtual_network_client.get_vnic(vnic_id).data
        
        logger.info(f"Instance public IP: {vnic.public_ip}")
        return vnic.public_ip
    except Exception as e:
        logger.error(f"Error getting instance IP: {str(e)}")
        return None

def provision_vm(config_file=None, compartment_id=None, display_name=None):
    """Provision a VM on Oracle Cloud Infrastructure."""
    start_time = datetime.now()
    logger.info(f"Starting VM provisioning at {start_time}")
    
    # Load configuration
    config = load_config(config_file)
    
    # Use compartment ID from environment if not provided
    if not compartment_id:
        compartment_id = os.environ.get("OCI_COMPARTMENT_OCID")
        if not compartment_id:
            logger.error("Compartment ID not provided and OCI_COMPARTMENT_OCID not set")
            sys.exit(1)
    
    # Use default display name if not provided
    if not display_name:
        display_name = f"GradientLab-VM-{int(time.time())}"
    
    # Initialize clients
    identity_client = IdentityClient(config)
    compute_client = ComputeClient(config)
    virtual_network_client = VirtualNetworkClient(config)
    
    # Get availability domains
    availability_domains = get_availability_domains(identity_client, compartment_id)
    if not availability_domains:
        logger.error("No availability domains found")
        sys.exit(1)
    
    # Create VCN
    vcn = create_vcn(virtual_network_client, compartment_id)
    
    # Create Internet Gateway
    ig = create_internet_gateway(virtual_network_client, compartment_id, vcn.id)
    
    # Update Route Table
    update_route_table(virtual_network_client, compartment_id, vcn.id, ig.id)
    
    # Create Security List
    security_list = create_security_list(virtual_network_client, compartment_id, vcn.id)
    
    # Create Subnet
    subnet = create_subnet(virtual_network_client, compartment_id, vcn.id, availability_domains[0])
    
    # Get Image
    image = get_image(compute_client, compartment_id)
    
    # Create Instance
    instance = create_instance(
        compute_client,
        compartment_id,
        availability_domains[0],
        subnet.id,
        image.id,
        display_name=display_name
    )
    
    # Get Instance IP
    ip_address = get_instance_ip(compute_client, virtual_network_client, instance.id)
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"VM provisioning completed at {end_time} (duration: {duration})")
    
    # Return VM details
    vm_details = {
        "id": instance.id,
        "name": instance.display_name,
        "compartment_id": instance.compartment_id,
        "availability_domain": instance.availability_domain,
        "shape": instance.shape,
        "lifecycle_state": instance.lifecycle_state,
        "time_created": instance.time_created.isoformat(),
        "ip_address": ip_address,
        "vcn_id": vcn.id,
        "subnet_id": subnet.id,
        "image_id": image.id
    }
    
    logger.info(f"VM details: {json.dumps(vm_details, indent=2)}")
    return vm_details

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provision a VM on Oracle Cloud Infrastructure")
    parser.add_argument("--config", help="Path to OCI config file")
    parser.add_argument("--compartment-id", help="OCI Compartment OCID")
    parser.add_argument("--display-name", help="Display name for the VM")
    args = parser.parse_args()
    
    vm_details = provision_vm(args.config, args.compartment_id, args.display_name)
    print(json.dumps(vm_details, indent=2))
