#!/usr/bin/env python3
"""
Script to set up scheduled tasks for monitoring and data collection.
This script creates cron jobs for monitoring nodes, performing POC taps, and collecting rewards.
"""
import os
import sys
import logging
import argparse
import subprocess
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scheduled_tasks.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_cron_job(command, schedule):
    """Create a cron job."""
    try:
        # Get current crontab
        result = subprocess.run(
            ["crontab", "-l"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        # If crontab doesn't exist, start with an empty one
        if result.returncode != 0:
            current_crontab = ""
        else:
            current_crontab = result.stdout
        
        # Check if the command already exists in the crontab
        if command in current_crontab:
            logger.info(f"Cron job already exists: {command}")
            return True
        
        # Add the new cron job
        new_crontab = current_crontab + f"{schedule} {command}\n"
        
        # Write the new crontab
        with open("/tmp/crontab", "w") as f:
            f.write(new_crontab)
        
        # Install the new crontab
        result = subprocess.run(
            ["crontab", "/tmp/crontab"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        logger.info(f"Cron job created: {schedule} {command}")
        return True
    except Exception as e:
        logger.error(f"Error creating cron job: {str(e)}")
        return False

def setup_monitoring_job(nodes_file, username="ubuntu", key_file=None, smtp_config=None):
    """Set up a cron job for monitoring nodes."""
    try:
        # Path to the monitoring script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monitor_nodes.py")
        
        # Build command
        command = f"{script_path} --nodes-file {nodes_file}"
        if username:
            command += f" --username {username}"
        if key_file:
            command += f" --key-file {key_file}"
        if smtp_config:
            command += f" --smtp-server {smtp_config['server']}"
            command += f" --smtp-port {smtp_config['port']}"
            command += f" --smtp-username {smtp_config['username']}"
            command += f" --smtp-password {smtp_config['password']}"
            command += f" --from-email {smtp_config['from']}"
            command += f" --to-email {smtp_config['to']}"
        
        # Schedule: every 5 minutes
        schedule = "*/5 * * * *"
        
        # Create cron job
        return create_cron_job(command, schedule)
    except Exception as e:
        logger.error(f"Error setting up monitoring job: {str(e)}")
        return False

def setup_poc_tap_job(nodes_file, username="ubuntu", key_file=None):
    """Set up a cron job for performing POC taps."""
    try:
        # Path to the POC tap script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "perform_poc_tap.py")
        
        # Build command
        command = f"{script_path} --nodes-file {nodes_file}"
        if username:
            command += f" --username {username}"
        if key_file:
            command += f" --key-file {key_file}"
        
        # Schedule: every 12 hours
        schedule = "0 */12 * * *"
        
        # Create cron job
        return create_cron_job(command, schedule)
    except Exception as e:
        logger.error(f"Error setting up POC tap job: {str(e)}")
        return False

def setup_reward_collection_job(nodes_file, db_file, api_url, api_key):
    """Set up a cron job for collecting rewards."""
    try:
        # Path to the reward collection script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "collect_rewards.py")
        
        # Build command
        command = f"{script_path} --nodes-file {nodes_file} --db-file {db_file} --api-url {api_url} --api-key {api_key}"
        
        # Schedule: every day at midnight
        schedule = "0 0 * * *"
        
        # Create cron job
        return create_cron_job(command, schedule)
    except Exception as e:
        logger.error(f"Error setting up reward collection job: {str(e)}")
        return False

def setup_data_analysis_job(nodes_file, db_file, output_dir):
    """Set up a cron job for analyzing data."""
    try:
        # Path to the data analysis script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analyze_data.py")
        
        # Build command
        command = f"{script_path} --nodes-file {nodes_file} --db-file {db_file} --output-dir {output_dir}"
        
        # Schedule: every day at 1 AM
        schedule = "0 1 * * *"
        
        # Create cron job
        return create_cron_job(command, schedule)
    except Exception as e:
        logger.error(f"Error setting up data analysis job: {str(e)}")
        return False

def setup_scheduled_tasks(nodes_file, db_file, output_dir, api_url, api_key, username="ubuntu", key_file=None, smtp_config=None):
    """Set up all scheduled tasks."""
    start_time = datetime.now()
    logger.info(f"Starting scheduled tasks setup at {start_time}")
    
    # Set up monitoring job
    if setup_monitoring_job(nodes_file, username, key_file, smtp_config):
        logger.info("Monitoring job set up successfully")
    else:
        logger.error("Failed to set up monitoring job")
    
    # Set up POC tap job
    if setup_poc_tap_job(nodes_file, username, key_file):
        logger.info("POC tap job set up successfully")
    else:
        logger.error("Failed to set up POC tap job")
    
    # Set up reward collection job
    if setup_reward_collection_job(nodes_file, db_file, api_url, api_key):
        logger.info("Reward collection job set up successfully")
    else:
        logger.error("Failed to set up reward collection job")
    
    # Set up data analysis job
    if setup_data_analysis_job(nodes_file, db_file, output_dir):
        logger.info("Data analysis job set up successfully")
    else:
        logger.error("Failed to set up data analysis job")
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"Scheduled tasks setup completed at {end_time} (duration: {duration})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up scheduled tasks for monitoring and data collection")
    parser.add_argument("--nodes-file", default="nodes.json", help="Path to nodes JSON file")
    parser.add_argument("--db-file", default="rewards.db", help="Path to rewards database file")
    parser.add_argument("--output-dir", default="reports", help="Path to output directory for reports")
    parser.add_argument("--api-url", required=True, help="Gradient Network API URL")
    parser.add_argument("--api-key", required=True, help="Gradient Network API key")
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
            "server": args.smtp_server,
            "port": args.smtp_port,
            "username": args.smtp_username,
            "password": args.smtp_password,
            "from": args.from_email,
            "to": args.to_email
        }
    
    setup_scheduled_tasks(
        args.nodes_file,
        args.db_file,
        args.output_dir,
        args.api_url,
        args.api_key,
        args.username,
        args.key_file,
        smtp_config
    )
