#!/usr/bin/env python3
"""
Script to install the Gradient Sentry Node extension on a VM.
This script connects to the VM via SSH and installs the extension.
"""
import os
import sys
import time
import json
import logging
import argparse
import subprocess
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sentry_node_install.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_ssh_connection(host, username="ubuntu", key_file=None, timeout=60):
    """Check if SSH connection to the host is possible."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            ssh_command = ["ssh"]
            if key_file:
                ssh_command.extend(["-i", key_file])
            ssh_command.extend([
                "-o", "StrictHostKeyChecking=no",
                "-o", "UserKnownHostsFile=/dev/null",
                "-o", "ConnectTimeout=5",
                f"{username}@{host}",
                "echo 'SSH connection successful'"
            ])
            
            result = subprocess.run(
                ssh_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                logger.info(f"SSH connection to {host} successful")
                return True
            
            logger.warning(f"SSH connection to {host} failed, retrying... ({result.stderr.strip()})")
            time.sleep(5)
        except Exception as e:
            logger.warning(f"Error checking SSH connection: {str(e)}")
            time.sleep(5)
    
    logger.error(f"SSH connection to {host} failed after {timeout} seconds")
    return False

def copy_setup_script(host, username="ubuntu", key_file=None):
    """Copy the setup script to the VM."""
    try:
        # Path to the setup script
        setup_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setup_vm.sh")
        
        # Copy the script to the VM
        scp_command = ["scp"]
        if key_file:
            scp_command.extend(["-i", key_file])
        scp_command.extend([
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            setup_script,
            f"{username}@{host}:/tmp/setup_vm.sh"
        ])
        
        result = subprocess.run(
            scp_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        logger.info(f"Setup script copied to {host}")
        return True
    except Exception as e:
        logger.error(f"Error copying setup script: {str(e)}")
        return False

def run_setup_script(host, username="ubuntu", key_file=None):
    """Run the setup script on the VM."""
    try:
        # Run the script on the VM
        ssh_command = ["ssh"]
        if key_file:
            ssh_command.extend(["-i", key_file])
        ssh_command.extend([
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            f"{username}@{host}",
            "sudo bash /tmp/setup_vm.sh"
        ])
        
        logger.info(f"Running setup script on {host}...")
        
        result = subprocess.run(
            ssh_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            logger.info(f"Setup script completed successfully on {host}")
            return True
        else:
            logger.error(f"Setup script failed on {host}: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error running setup script: {str(e)}")
        return False

def check_sentry_node_status(host, username="ubuntu", key_file=None):
    """Check the status of the Sentry Node on the VM."""
    try:
        # Check if Chromium is running
        ssh_command = ["ssh"]
        if key_file:
            ssh_command.extend(["-i", key_file])
        ssh_command.extend([
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            f"{username}@{host}",
            "pgrep -f 'chromium-browser --headless' > /dev/null && echo 'running' || echo 'stopped'"
        ])
        
        result = subprocess.run(
            ssh_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        status = result.stdout.strip()
        logger.info(f"Sentry Node status on {host}: {status}")
        
        return status == "running"
    except Exception as e:
        logger.error(f"Error checking Sentry Node status: {str(e)}")
        return False

def install_sentry_node(host, username="ubuntu", key_file=None, timeout=300):
    """Install the Sentry Node extension on a VM."""
    start_time = datetime.now()
    logger.info(f"Starting Sentry Node installation on {host} at {start_time}")
    
    # Check SSH connection
    if not check_ssh_connection(host, username, key_file):
        logger.error(f"Cannot connect to {host} via SSH")
        return False
    
    # Copy setup script
    if not copy_setup_script(host, username, key_file):
        logger.error(f"Failed to copy setup script to {host}")
        return False
    
    # Run setup script
    if not run_setup_script(host, username, key_file):
        logger.error(f"Failed to run setup script on {host}")
        return False
    
    # Check Sentry Node status
    if not check_sentry_node_status(host, username, key_file):
        logger.error(f"Sentry Node is not running on {host}")
        return False
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"Sentry Node installation completed on {host} at {end_time} (duration: {duration})")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install the Gradient Sentry Node extension on a VM")
    parser.add_argument("host", help="Hostname or IP address of the VM")
    parser.add_argument("--username", default="ubuntu", help="SSH username")
    parser.add_argument("--key-file", help="Path to SSH private key file")
    args = parser.parse_args()
    
    success = install_sentry_node(args.host, args.username, args.key_file)
    sys.exit(0 if success else 1)
