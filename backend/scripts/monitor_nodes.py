#!/usr/bin/env python3
"""
Script to monitor Gradient Sentry Nodes.
This script checks the status of all nodes and sends alerts if any are down.
"""
import os
import sys
import json
import time
import logging
import argparse
import requests
import subprocess
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("node_monitoring.log"),
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

def check_node_status(node):
    """Check the status of a node."""
    try:
        # Try to access the status page
        url = f"http://{node['ip_address']}/status.json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            status = response.json()
            logger.info(f"Node {node['name']} ({node['ip_address']}) status: {status['running']}")
            return status
        else:
            logger.warning(f"Node {node['name']} ({node['ip_address']}) returned status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.warning(f"Error checking node {node['name']} ({node['ip_address']}): {str(e)}")
        return None

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

def restart_node_service(node, username="ubuntu", key_file=None):
    """Restart the Sentry Node service on a node."""
    try:
        ssh_command = ["ssh"]
        if key_file:
            ssh_command.extend(["-i", key_file])
        ssh_command.extend([
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            f"{username}@{node['ip_address']}",
            "sudo systemctl restart chromium"
        ])
        
        result = subprocess.run(
            ssh_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            logger.info(f"Restarted Sentry Node service on {node['name']} ({node['ip_address']})")
            return True
        
        logger.warning(f"Failed to restart Sentry Node service on {node['name']} ({node['ip_address']}): {result.stderr.strip()}")
        return False
    except Exception as e:
        logger.warning(f"Error restarting Sentry Node service on {node['name']} ({node['ip_address']}): {str(e)}")
        return False

def send_email_alert(node, status, smtp_server, smtp_port, smtp_username, smtp_password, from_email, to_email):
    """Send an email alert for a node that is down."""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = f"ALERT: Gradient Sentry Node {node['name']} is DOWN"
        
        # Create message body
        body = f"""
        <html>
        <body>
            <h2>Gradient Sentry Node Alert</h2>
            <p>The following Sentry Node is DOWN:</p>
            <ul>
                <li><strong>Name:</strong> {node['name']}</li>
                <li><strong>IP Address:</strong> {node['ip_address']}</li>
                <li><strong>Provider:</strong> {node['provider']}</li>
                <li><strong>Region:</strong> {node['region']}</li>
                <li><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            <p>Automatic recovery has been attempted.</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to SMTP server and send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Sent email alert for node {node['name']} ({node['ip_address']})")
        return True
    except Exception as e:
        logger.error(f"Error sending email alert for node {node['name']} ({node['ip_address']}): {str(e)}")
        return False

def update_node_status(node, status, nodes_file):
    """Update the status of a node in the nodes file."""
    try:
        # Load current nodes
        with open(nodes_file, 'r') as f:
            nodes = json.load(f)
        
        # Find the node and update its status
        for n in nodes:
            if n['id'] == node['id']:
                n['status'] = 'running' if status and status.get('running', False) else 'stopped'
                n['last_checked'] = datetime.now().isoformat()
                n['uptime_percentage'] = calculate_uptime(n)
                break
        
        # Save updated nodes
        with open(nodes_file, 'w') as f:
            json.dump(nodes, f, indent=2)
        
        logger.info(f"Updated status of node {node['name']} ({node['ip_address']}) to {n['status']}")
        return True
    except Exception as e:
        logger.error(f"Error updating status of node {node['name']} ({node['ip_address']}): {str(e)}")
        return False

def calculate_uptime(node):
    """Calculate the uptime percentage of a node."""
    try:
        # Get the uptime history
        uptime_history = node.get('uptime_history', [])
        
        # If no history, return 0
        if not uptime_history:
            return 0
        
        # Calculate uptime percentage
        up_count = sum(1 for status in uptime_history if status == 'running')
        total_count = len(uptime_history)
        
        return round((up_count / total_count) * 100, 2)
    except Exception as e:
        logger.error(f"Error calculating uptime for node {node['name']}: {str(e)}")
        return 0

def update_uptime_history(node, status, nodes_file):
    """Update the uptime history of a node."""
    try:
        # Load current nodes
        with open(nodes_file, 'r') as f:
            nodes = json.load(f)
        
        # Find the node and update its uptime history
        for n in nodes:
            if n['id'] == node['id']:
                # Initialize uptime history if it doesn't exist
                if 'uptime_history' not in n:
                    n['uptime_history'] = []
                
                # Add current status to history (limit to last 1000 entries)
                n['uptime_history'].append('running' if status and status.get('running', False) else 'stopped')
                n['uptime_history'] = n['uptime_history'][-1000:]
                
                # Update uptime percentage
                n['uptime_percentage'] = calculate_uptime(n)
                break
        
        # Save updated nodes
        with open(nodes_file, 'w') as f:
            json.dump(nodes, f, indent=2)
        
        logger.info(f"Updated uptime history of node {node['name']} ({node['ip_address']})")
        return True
    except Exception as e:
        logger.error(f"Error updating uptime history of node {node['name']} ({node['ip_address']}): {str(e)}")
        return False

def monitor_nodes(nodes_file, username="ubuntu", key_file=None, smtp_config=None):
    """Monitor all nodes and take action if any are down."""
    start_time = datetime.now()
    logger.info(f"Starting node monitoring at {start_time}")
    
    # Load nodes
    nodes = load_nodes(nodes_file)
    if not nodes:
        logger.error(f"No nodes found in {nodes_file}")
        return
    
    # Check each node
    for node in nodes:
        logger.info(f"Checking node {node['name']} ({node['ip_address']})")
        
        # Check node status
        status = check_node_status(node)
        
        # Update uptime history
        update_uptime_history(node, status, nodes_file)
        
        # If node is down, try to restart it
        if not status or not status.get('running', False):
            logger.warning(f"Node {node['name']} ({node['ip_address']}) is DOWN")
            
            # Check SSH connection
            if check_ssh_connection(node, username, key_file):
                # Try to restart the service
                restart_node_service(node, username, key_file)
                
                # Check status again after restart
                time.sleep(10)
                status = check_node_status(node)
                
                # Update status
                update_node_status(node, status, nodes_file)
                
                # If still down, send alert
                if not status or not status.get('running', False):
                    logger.error(f"Node {node['name']} ({node['ip_address']}) is still DOWN after restart")
                    
                    # Send email alert if configured
                    if smtp_config:
                        send_email_alert(node, status, **smtp_config)
            else:
                logger.error(f"Cannot connect to node {node['name']} ({node['ip_address']}) via SSH")
                
                # Update status
                update_node_status(node, None, nodes_file)
                
                # Send email alert if configured
                if smtp_config:
                    send_email_alert(node, None, **smtp_config)
        else:
            logger.info(f"Node {node['name']} ({node['ip_address']}) is UP")
            
            # Update status
            update_node_status(node, status, nodes_file)
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"Node monitoring completed at {end_time} (duration: {duration})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor Gradient Sentry Nodes")
    parser.add_argument("--nodes-file", default="nodes.json", help="Path to nodes JSON file")
    parser.add_argument("--username", default="ubuntu", help="SSH username")
    parser.add_argument("--key-file", help="Path to SSH private key file")
    parser.add_argument("--smtp-server", help="SMTP server for email alerts")
    parser.add_argument("--smtp-port", type=int, default=587, help="SMTP port")
    parser.add_argument("--smtp-username", help="SMTP username")
    parser.add_argument("--smtp-password", help="SMTP password")
    parser.add_argument("--from-email", help="From email address")
    parser.add_argument("--to-email", help="To email address")
    args = parser.parse_args()
    
    # Set up SMTP config if email alerts are enabled
    smtp_config = None
    if args.smtp_server and args.smtp_username and args.smtp_password and args.from_email and args.to_email:
        smtp_config = {
            "smtp_server": args.smtp_server,
            "smtp_port": args.smtp_port,
            "smtp_username": args.smtp_username,
            "smtp_password": args.smtp_password,
            "from_email": args.from_email,
            "to_email": args.to_email
        }
    
    monitor_nodes(args.nodes_file, args.username, args.key_file, smtp_config)
