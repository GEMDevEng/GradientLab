#!/usr/bin/env python3
"""
Script to perform POC taps on Gradient Sentry Nodes.
This script connects to each node and performs a POC tap.
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
        logging.FileHandler("poc_tap.log"),
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

def perform_poc_tap(node, username="ubuntu", key_file=None):
    """Perform a POC tap on a node."""
    try:
        ssh_command = ["ssh"]
        if key_file:
            ssh_command.extend(["-i", key_file])
        ssh_command.extend([
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            f"{username}@{node['ip_address']}",
            "sudo /home/gradient/sentry/poc_tap.sh"
        ])
        
        result = subprocess.run(
            ssh_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            logger.info(f"POC tap performed on {node['name']} ({node['ip_address']})")
            return True
        
        logger.warning(f"Failed to perform POC tap on {node['name']} ({node['ip_address']}): {result.stderr.strip()}")
        return False
    except Exception as e:
        logger.warning(f"Error performing POC tap on {node['name']} ({node['ip_address']}): {str(e)}")
        return False

def update_poc_history(node, success, nodes_file):
    """Update the POC tap history of a node."""
    try:
        # Load current nodes
        with open(nodes_file, 'r') as f:
            nodes = json.load(f)
        
        # Find the node and update its POC tap history
        for n in nodes:
            if n['id'] == node['id']:
                # Initialize POC tap history if it doesn't exist
                if 'poc_history' not in n:
                    n['poc_history'] = []
                
                # Add current POC tap to history
                n['poc_history'].append({
                    'timestamp': datetime.now().isoformat(),
                    'success': success
                })
                
                # Limit history to last 100 entries
                n['poc_history'] = n['poc_history'][-100:]
                
                # Update POC tap success rate
                n['poc_success_rate'] = calculate_poc_success_rate(n)
                break
        
        # Save updated nodes
        with open(nodes_file, 'w') as f:
            json.dump(nodes, f, indent=2)
        
        logger.info(f"Updated POC tap history of node {node['name']} ({node['ip_address']})")
        return True
    except Exception as e:
        logger.error(f"Error updating POC tap history of node {node['name']} ({node['ip_address']}): {str(e)}")
        return False

def calculate_poc_success_rate(node):
    """Calculate the POC tap success rate of a node."""
    try:
        # Get the POC tap history
        poc_history = node.get('poc_history', [])
        
        # If no history, return 0
        if not poc_history:
            return 0
        
        # Calculate success rate
        success_count = sum(1 for tap in poc_history if tap.get('success', False))
        total_count = len(poc_history)
        
        return round((success_count / total_count) * 100, 2)
    except Exception as e:
        logger.error(f"Error calculating POC success rate for node {node['name']}: {str(e)}")
        return 0

def perform_poc_taps(nodes_file, username="ubuntu", key_file=None):
    """Perform POC taps on all nodes."""
    start_time = datetime.now()
    logger.info(f"Starting POC taps at {start_time}")
    
    # Load nodes
    nodes = load_nodes(nodes_file)
    if not nodes:
        logger.error(f"No nodes found in {nodes_file}")
        return
    
    # Perform POC tap on each node
    for node in nodes:
        logger.info(f"Performing POC tap on node {node['name']} ({node['ip_address']})")
        
        # Check if node is running
        if node.get('status') != 'running':
            logger.warning(f"Node {node['name']} ({node['ip_address']}) is not running, skipping POC tap")
            continue
        
        # Check SSH connection
        if check_ssh_connection(node, username, key_file):
            # Perform POC tap
            success = perform_poc_tap(node, username, key_file)
            
            # Update POC tap history
            update_poc_history(node, success, nodes_file)
        else:
            logger.error(f"Cannot connect to node {node['name']} ({node['ip_address']}) via SSH")
            
            # Update POC tap history (failed)
            update_poc_history(node, False, nodes_file)
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"POC taps completed at {end_time} (duration: {duration})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform POC taps on Gradient Sentry Nodes")
    parser.add_argument("--nodes-file", default="nodes.json", help="Path to nodes JSON file")
    parser.add_argument("--username", default="ubuntu", help="SSH username")
    parser.add_argument("--key-file", help="Path to SSH private key file")
    args = parser.parse_args()
    
    perform_poc_taps(args.nodes_file, args.username, args.key_file)
