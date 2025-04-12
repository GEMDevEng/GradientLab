#!/usr/bin/env python3
"""
Script to check if the Heroku deployment is ready.
This script checks if the Heroku app is running and the API is accessible.
"""
import os
import sys
import time
import json
import logging
import argparse
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("heroku_check.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_heroku_app(app_name, max_retries=10, retry_interval=5):
    """Check if the Heroku app is running and the API is accessible."""
    url = f"https://{app_name}.herokuapp.com/api/health"
    
    for i in range(max_retries):
        try:
            logger.info(f"Checking Heroku app: {app_name} (attempt {i+1}/{max_retries})")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    logger.info(f"Heroku app {app_name} is running and healthy")
                    return True
                else:
                    logger.warning(f"Heroku app {app_name} returned unexpected response: {data}")
            else:
                logger.warning(f"Heroku app {app_name} returned status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error checking Heroku app {app_name}: {str(e)}")
        
        if i < max_retries - 1:
            logger.info(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    
    logger.error(f"Heroku app {app_name} is not running or not accessible after {max_retries} attempts")
    return False

def check_database_initialization(app_name, max_retries=5, retry_interval=5):
    """Check if the database is initialized."""
    url = f"https://{app_name}.herokuapp.com/api/auth/status"
    
    for i in range(max_retries):
        try:
            logger.info(f"Checking database initialization: {app_name} (attempt {i+1}/{max_retries})")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success' and data.get('data', {}).get('database_initialized'):
                    logger.info(f"Database for {app_name} is initialized")
                    return True
                else:
                    logger.warning(f"Database for {app_name} is not initialized: {data}")
            else:
                logger.warning(f"Database check for {app_name} returned status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error checking database for {app_name}: {str(e)}")
        
        if i < max_retries - 1:
            logger.info(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    
    logger.error(f"Database for {app_name} is not initialized or not accessible after {max_retries} attempts")
    return False

def check_heroku_deployment(app_name, max_retries=10, retry_interval=5):
    """Check if the Heroku deployment is ready."""
    start_time = datetime.now()
    logger.info(f"Starting Heroku deployment check at {start_time}")
    
    # Check if the app is running
    if not check_heroku_app(app_name, max_retries, retry_interval):
        logger.error(f"Heroku app {app_name} is not running or not accessible")
        return False
    
    # Check if the database is initialized
    if not check_database_initialization(app_name, max_retries, retry_interval):
        logger.error(f"Database for {app_name} is not initialized or not accessible")
        return False
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"Heroku deployment check completed at {end_time} (duration: {duration})")
    logger.info(f"Heroku app {app_name} is running and ready")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if the Heroku deployment is ready")
    parser.add_argument("app_name", help="Heroku app name")
    parser.add_argument("--max-retries", type=int, default=10, help="Maximum number of retries")
    parser.add_argument("--retry-interval", type=int, default=5, help="Retry interval in seconds")
    args = parser.parse_args()
    
    success = check_heroku_deployment(args.app_name, args.max_retries, args.retry_interval)
    sys.exit(0 if success else 1)
