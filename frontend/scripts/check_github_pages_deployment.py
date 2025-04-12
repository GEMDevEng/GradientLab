#!/usr/bin/env python3
"""
Script to check if the GitHub Pages deployment is ready.
This script checks if the GitHub Pages site is accessible.
"""
import os
import sys
import time
import logging
import argparse
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("github_pages_check.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_github_pages(repo_owner, repo_name, max_retries=10, retry_interval=5):
    """Check if the GitHub Pages site is accessible."""
    url = f"https://{repo_owner}.github.io/{repo_name}"
    
    for i in range(max_retries):
        try:
            logger.info(f"Checking GitHub Pages site: {url} (attempt {i+1}/{max_retries})")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"GitHub Pages site {url} is accessible")
                return True
            else:
                logger.warning(f"GitHub Pages site {url} returned status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error checking GitHub Pages site {url}: {str(e)}")
        
        if i < max_retries - 1:
            logger.info(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    
    logger.error(f"GitHub Pages site {url} is not accessible after {max_retries} attempts")
    return False

def check_api_connection(repo_owner, repo_name, api_url, max_retries=5, retry_interval=5):
    """Check if the frontend can connect to the API."""
    frontend_url = f"https://{repo_owner}.github.io/{repo_name}"
    
    for i in range(max_retries):
        try:
            logger.info(f"Checking API connection from {frontend_url} to {api_url} (attempt {i+1}/{max_retries})")
            
            # This is a simplified check - in a real scenario, you would need to
            # check if the frontend can actually connect to the API, which might
            # require browser automation or checking CORS headers
            response = requests.get(api_url, headers={
                "Origin": frontend_url
            }, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"API connection from {frontend_url} to {api_url} is working")
                return True
            else:
                logger.warning(f"API connection check returned status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error checking API connection: {str(e)}")
        
        if i < max_retries - 1:
            logger.info(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    
    logger.error(f"API connection from {frontend_url} to {api_url} is not working after {max_retries} attempts")
    return False

def check_github_pages_deployment(repo_owner, repo_name, api_url=None, max_retries=10, retry_interval=5):
    """Check if the GitHub Pages deployment is ready."""
    start_time = datetime.now()
    logger.info(f"Starting GitHub Pages deployment check at {start_time}")
    
    # Check if the site is accessible
    if not check_github_pages(repo_owner, repo_name, max_retries, retry_interval):
        logger.error(f"GitHub Pages site https://{repo_owner}.github.io/{repo_name} is not accessible")
        return False
    
    # Check if the frontend can connect to the API (if provided)
    if api_url:
        if not check_api_connection(repo_owner, repo_name, api_url, max_retries, retry_interval):
            logger.error(f"API connection to {api_url} is not working")
            return False
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"GitHub Pages deployment check completed at {end_time} (duration: {duration})")
    logger.info(f"GitHub Pages site https://{repo_owner}.github.io/{repo_name} is accessible and ready")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if the GitHub Pages deployment is ready")
    parser.add_argument("repo_owner", help="GitHub repository owner")
    parser.add_argument("repo_name", help="GitHub repository name")
    parser.add_argument("--api-url", help="API URL to check connection to")
    parser.add_argument("--max-retries", type=int, default=10, help="Maximum number of retries")
    parser.add_argument("--retry-interval", type=int, default=5, help="Retry interval in seconds")
    args = parser.parse_args()
    
    success = check_github_pages_deployment(
        args.repo_owner,
        args.repo_name,
        args.api_url,
        args.max_retries,
        args.retry_interval
    )
    sys.exit(0 if success else 1)
