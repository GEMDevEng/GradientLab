#!/usr/bin/env python3
"""
Script to enhance the security of Gradient Sentry Node VMs.
This script connects to each VM and applies security hardening measures.
"""
import os
import sys
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
        logging.FileHandler("security_enhancement.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_nodes(nodes_file):
    """Load nodes from a JSON file."""
    try:
        with open(nodes_file, 'r') as f:
            nodes = json.load(f)
        logger.info(f"Loaded {len(nodes)} nodes from {nodes_file}")
        return nodes
    except Exception as e:
        logger.error(f"Error loading nodes from {nodes_file}: {str(e)}")
        return []

def check_ssh_connection(node, username="ubuntu", key_file=None):
    """Check if SSH connection to the node is possible."""
    try:
        ssh_command = ["ssh"]
        if key_file:
            ssh_command.extend(["-i", key_file])
        ssh_command.extend([
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "ConnectTimeout=5",
            f"{username}@{node['ip_address']}",
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
            logger.info(f"SSH connection to {node['name']} ({node['ip_address']}) successful")
            return True
        
        logger.warning(f"SSH connection to {node['name']} ({node['ip_address']}) failed: {result.stderr.strip()}")
        return False
    except Exception as e:
        logger.warning(f"Error checking SSH connection to {node['name']} ({node['ip_address']}): {str(e)}")
        return False

def run_ssh_command(node, command, username="ubuntu", key_file=None):
    """Run a command on a node via SSH."""
    try:
        ssh_command = ["ssh"]
        if key_file:
            ssh_command.extend(["-i", key_file])
        ssh_command.extend([
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            f"{username}@{node['ip_address']}",
            command
        ])
        
        result = subprocess.run(
            ssh_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            logger.info(f"Command executed successfully on {node['name']} ({node['ip_address']}): {command}")
            return result.stdout.strip()
        else:
            logger.warning(f"Command failed on {node['name']} ({node['ip_address']}): {command}")
            logger.warning(f"Error: {result.stderr.strip()}")
            return None
    except Exception as e:
        logger.warning(f"Error running command on {node['name']} ({node['ip_address']}): {str(e)}")
        return None

def copy_file_to_node(node, local_file, remote_file, username="ubuntu", key_file=None):
    """Copy a file to a node via SCP."""
    try:
        scp_command = ["scp"]
        if key_file:
            scp_command.extend(["-i", key_file])
        scp_command.extend([
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            local_file,
            f"{username}@{node['ip_address']}:{remote_file}"
        ])
        
        result = subprocess.run(
            scp_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            logger.info(f"File copied successfully to {node['name']} ({node['ip_address']}): {local_file} -> {remote_file}")
            return True
        else:
            logger.warning(f"File copy failed to {node['name']} ({node['ip_address']}): {local_file} -> {remote_file}")
            logger.warning(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        logger.warning(f"Error copying file to {node['name']} ({node['ip_address']}): {str(e)}")
        return False

def update_system(node, username="ubuntu", key_file=None):
    """Update the system packages."""
    logger.info(f"Updating system packages on {node['name']} ({node['ip_address']})")
    
    # Determine the OS type
    os_type = run_ssh_command(node, "cat /etc/os-release | grep -E '^ID=' | cut -d= -f2", username, key_file)
    
    if os_type:
        os_type = os_type.strip('"\'')
        
        if os_type in ["ubuntu", "debian"]:
            # Ubuntu/Debian
            run_ssh_command(node, "sudo apt update && sudo apt upgrade -y", username, key_file)
        elif os_type in ["rhel", "centos", "ol", "fedora"]:
            # RHEL/CentOS/Oracle Linux/Fedora
            run_ssh_command(node, "sudo yum update -y", username, key_file)
        else:
            logger.warning(f"Unsupported OS type on {node['name']} ({node['ip_address']}): {os_type}")
            return False
        
        logger.info(f"System packages updated on {node['name']} ({node['ip_address']})")
        return True
    else:
        logger.warning(f"Could not determine OS type on {node['name']} ({node['ip_address']})")
        return False

def configure_firewall(node, username="ubuntu", key_file=None):
    """Configure the firewall to allow only necessary ports."""
    logger.info(f"Configuring firewall on {node['name']} ({node['ip_address']})")
    
    # Determine the OS type
    os_type = run_ssh_command(node, "cat /etc/os-release | grep -E '^ID=' | cut -d= -f2", username, key_file)
    
    if os_type:
        os_type = os_type.strip('"\'')
        
        if os_type in ["ubuntu", "debian"]:
            # Ubuntu/Debian
            run_ssh_command(node, "sudo apt install -y ufw", username, key_file)
            run_ssh_command(node, "sudo ufw allow 22/tcp", username, key_file)
            run_ssh_command(node, "sudo ufw allow 80/tcp", username, key_file)
            run_ssh_command(node, "sudo ufw allow 443/tcp", username, key_file)
            run_ssh_command(node, "sudo ufw --force enable", username, key_file)
        elif os_type in ["rhel", "centos", "ol", "fedora"]:
            # RHEL/CentOS/Oracle Linux/Fedora
            run_ssh_command(node, "sudo yum install -y firewalld", username, key_file)
            run_ssh_command(node, "sudo systemctl enable firewalld", username, key_file)
            run_ssh_command(node, "sudo systemctl start firewalld", username, key_file)
            run_ssh_command(node, "sudo firewall-cmd --permanent --add-service=ssh", username, key_file)
            run_ssh_command(node, "sudo firewall-cmd --permanent --add-service=http", username, key_file)
            run_ssh_command(node, "sudo firewall-cmd --permanent --add-service=https", username, key_file)
            run_ssh_command(node, "sudo firewall-cmd --reload", username, key_file)
        else:
            logger.warning(f"Unsupported OS type on {node['name']} ({node['ip_address']}): {os_type}")
            return False
        
        logger.info(f"Firewall configured on {node['name']} ({node['ip_address']})")
        return True
    else:
        logger.warning(f"Could not determine OS type on {node['name']} ({node['ip_address']})")
        return False

def secure_ssh(node, username="ubuntu", key_file=None):
    """Secure SSH configuration."""
    logger.info(f"Securing SSH on {node['name']} ({node['ip_address']})")
    
    # Create a temporary sshd_config file
    with open("sshd_config.tmp", "w") as f:
        f.write("""# SSH configuration hardened for security
Port 22
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key
UsePrivilegeSeparation yes
KeyRegenerationInterval 3600
ServerKeyBits 2048
SyslogFacility AUTH
LogLevel INFO
LoginGraceTime 120
PermitRootLogin no
StrictModes yes
RSAAuthentication yes
PubkeyAuthentication yes
IgnoreRhosts yes
RhostsRSAAuthentication no
HostbasedAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
PasswordAuthentication no
X11Forwarding no
X11DisplayOffset 10
PrintMotd no
PrintLastLog yes
TCPKeepAlive yes
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
UsePAM yes
AllowUsers %s
""" % username)
    
    # Copy the file to the node
    if copy_file_to_node(node, "sshd_config.tmp", "/tmp/sshd_config", username, key_file):
        # Move the file to /etc/ssh/sshd_config
        run_ssh_command(node, "sudo cp /tmp/sshd_config /etc/ssh/sshd_config", username, key_file)
        run_ssh_command(node, "sudo chmod 644 /etc/ssh/sshd_config", username, key_file)
        run_ssh_command(node, "sudo systemctl restart sshd", username, key_file)
        
        # Remove the temporary file
        os.remove("sshd_config.tmp")
        
        logger.info(f"SSH secured on {node['name']} ({node['ip_address']})")
        return True
    else:
        logger.warning(f"Failed to secure SSH on {node['name']} ({node['ip_address']})")
        return False

def install_security_updates_automatically(node, username="ubuntu", key_file=None):
    """Configure automatic security updates."""
    logger.info(f"Setting up automatic security updates on {node['name']} ({node['ip_address']})")
    
    # Determine the OS type
    os_type = run_ssh_command(node, "cat /etc/os-release | grep -E '^ID=' | cut -d= -f2", username, key_file)
    
    if os_type:
        os_type = os_type.strip('"\'')
        
        if os_type in ["ubuntu", "debian"]:
            # Ubuntu/Debian
            run_ssh_command(node, "sudo apt install -y unattended-upgrades apt-listchanges", username, key_file)
            run_ssh_command(node, "echo 'Unattended-Upgrade::Allowed-Origins { \"${distro_id}:${distro_codename}\"; \"${distro_id}:${distro_codename}-security\"; };' | sudo tee /etc/apt/apt.conf.d/50unattended-upgrades", username, key_file)
            run_ssh_command(node, "echo 'Unattended-Upgrade::Package-Blacklist {};' | sudo tee -a /etc/apt/apt.conf.d/50unattended-upgrades", username, key_file)
            run_ssh_command(node, "echo 'Unattended-Upgrade::AutoFixInterruptedDpkg \"true\";' | sudo tee -a /etc/apt/apt.conf.d/50unattended-upgrades", username, key_file)
            run_ssh_command(node, "echo 'APT::Periodic::Update-Package-Lists \"1\";' | sudo tee /etc/apt/apt.conf.d/20auto-upgrades", username, key_file)
            run_ssh_command(node, "echo 'APT::Periodic::Unattended-Upgrade \"1\";' | sudo tee -a /etc/apt/apt.conf.d/20auto-upgrades", username, key_file)
        elif os_type in ["rhel", "centos", "ol", "fedora"]:
            # RHEL/CentOS/Oracle Linux/Fedora
            run_ssh_command(node, "sudo yum install -y yum-cron", username, key_file)
            run_ssh_command(node, "sudo sed -i 's/apply_updates = no/apply_updates = yes/g' /etc/yum/yum-cron.conf", username, key_file)
            run_ssh_command(node, "sudo systemctl enable yum-cron", username, key_file)
            run_ssh_command(node, "sudo systemctl start yum-cron", username, key_file)
        else:
            logger.warning(f"Unsupported OS type on {node['name']} ({node['ip_address']}): {os_type}")
            return False
        
        logger.info(f"Automatic security updates configured on {node['name']} ({node['ip_address']})")
        return True
    else:
        logger.warning(f"Could not determine OS type on {node['name']} ({node['ip_address']})")
        return False

def install_fail2ban(node, username="ubuntu", key_file=None):
    """Install and configure fail2ban."""
    logger.info(f"Installing fail2ban on {node['name']} ({node['ip_address']})")
    
    # Determine the OS type
    os_type = run_ssh_command(node, "cat /etc/os-release | grep -E '^ID=' | cut -d= -f2", username, key_file)
    
    if os_type:
        os_type = os_type.strip('"\'')
        
        if os_type in ["ubuntu", "debian"]:
            # Ubuntu/Debian
            run_ssh_command(node, "sudo apt install -y fail2ban", username, key_file)
        elif os_type in ["rhel", "centos", "ol", "fedora"]:
            # RHEL/CentOS/Oracle Linux/Fedora
            run_ssh_command(node, "sudo yum install -y epel-release", username, key_file)
            run_ssh_command(node, "sudo yum install -y fail2ban", username, key_file)
        else:
            logger.warning(f"Unsupported OS type on {node['name']} ({node['ip_address']}): {os_type}")
            return False
        
        # Configure fail2ban
        run_ssh_command(node, "echo '[sshd]' | sudo tee /etc/fail2ban/jail.local", username, key_file)
        run_ssh_command(node, "echo 'enabled = true' | sudo tee -a /etc/fail2ban/jail.local", username, key_file)
        run_ssh_command(node, "echo 'port = ssh' | sudo tee -a /etc/fail2ban/jail.local", username, key_file)
        run_ssh_command(node, "echo 'filter = sshd' | sudo tee -a /etc/fail2ban/jail.local", username, key_file)
        run_ssh_command(node, "echo 'logpath = /var/log/auth.log' | sudo tee -a /etc/fail2ban/jail.local", username, key_file)
        run_ssh_command(node, "echo 'maxretry = 3' | sudo tee -a /etc/fail2ban/jail.local", username, key_file)
        run_ssh_command(node, "echo 'bantime = 3600' | sudo tee -a /etc/fail2ban/jail.local", username, key_file)
        
        # Enable and start fail2ban
        run_ssh_command(node, "sudo systemctl enable fail2ban", username, key_file)
        run_ssh_command(node, "sudo systemctl start fail2ban", username, key_file)
        
        logger.info(f"fail2ban installed and configured on {node['name']} ({node['ip_address']})")
        return True
    else:
        logger.warning(f"Could not determine OS type on {node['name']} ({node['ip_address']})")
        return False

def secure_file_permissions(node, username="ubuntu", key_file=None):
    """Secure file permissions for sensitive files."""
    logger.info(f"Securing file permissions on {node['name']} ({node['ip_address']})")
    
    # Secure gradient directory
    run_ssh_command(node, "sudo chmod 700 /home/gradient", username, key_file)
    run_ssh_command(node, "sudo chmod 700 /home/gradient/sentry", username, key_file)
    
    # Secure configuration files
    run_ssh_command(node, "sudo chmod 600 /home/gradient/sentry/config.json", username, key_file)
    run_ssh_command(node, "sudo chmod 600 /home/gradient/sentry/*.sh", username, key_file)
    
    # Secure log files
    run_ssh_command(node, "sudo chmod 640 /home/gradient/sentry/*.log", username, key_file)
    
    logger.info(f"File permissions secured on {node['name']} ({node['ip_address']})")
    return True

def enhance_vm_security(nodes_file, username="ubuntu", key_file=None):
    """Enhance the security of all VMs."""
    start_time = datetime.now()
    logger.info(f"Starting security enhancement at {start_time}")
    
    # Load nodes
    nodes = load_nodes(nodes_file)
    if not nodes:
        logger.error(f"No nodes found in {nodes_file}")
        return
    
    # Enhance security for each node
    for node in nodes:
        logger.info(f"Enhancing security for {node['name']} ({node['ip_address']})")
        
        # Check SSH connection
        if not check_ssh_connection(node, username, key_file):
            logger.error(f"Cannot connect to {node['name']} ({node['ip_address']}) via SSH")
            continue
        
        # Update system
        update_system(node, username, key_file)
        
        # Configure firewall
        configure_firewall(node, username, key_file)
        
        # Secure SSH
        secure_ssh(node, username, key_file)
        
        # Install automatic security updates
        install_security_updates_automatically(node, username, key_file)
        
        # Install fail2ban
        install_fail2ban(node, username, key_file)
        
        # Secure file permissions
        secure_file_permissions(node, username, key_file)
        
        logger.info(f"Security enhanced for {node['name']} ({node['ip_address']})")
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"Security enhancement completed at {end_time} (duration: {duration})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhance the security of Gradient Sentry Node VMs")
    parser.add_argument("--nodes-file", default="nodes.json", help="Path to nodes JSON file")
    parser.add_argument("--username", default="ubuntu", help="SSH username")
    parser.add_argument("--key-file", help="Path to SSH private key file")
    args = parser.parse_args()
    
    enhance_vm_security(args.nodes_file, args.username, args.key_file)
