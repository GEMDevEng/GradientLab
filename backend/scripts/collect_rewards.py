#!/usr/bin/env python3
"""
Script to collect reward data from the Gradient Network.
This script queries the Gradient Network API for reward data and stores it in a database.
"""
import os
import sys
import json
import time
import logging
import argparse
import requests
from datetime import datetime, timedelta
import sqlite3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("reward_collection.log"),
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

def initialize_database(db_file):
    """Initialize the rewards database."""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Create rewards table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS rewards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_id TEXT NOT NULL,
            date TEXT NOT NULL,
            poa_points REAL NOT NULL,
            poc_points REAL NOT NULL,
            referral_points REAL NOT NULL,
            total_points REAL NOT NULL,
            created_at TEXT NOT NULL
        )
        ''')
        
        # Create daily_rewards table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_rewards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            poa_points REAL NOT NULL,
            poc_points REAL NOT NULL,
            referral_points REAL NOT NULL,
            total_points REAL NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(date)
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info(f"Database initialized: {db_file}")
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False

def get_rewards_from_api(api_url, api_key, node_id, start_date, end_date):
    """Get rewards from the Gradient Network API."""
    try:
        # Set up API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        params = {
            "node_id": node_id,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        
        # Make API request
        response = requests.get(f"{api_url}/rewards", headers=headers, params=params)
        
        if response.status_code == 200:
            rewards = response.json()
            logger.info(f"Got rewards for node {node_id} from {start_date} to {end_date}")
            return rewards
        else:
            logger.warning(f"Failed to get rewards for node {node_id}: {response.status_code} {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error getting rewards for node {node_id}: {str(e)}")
        return None

def store_rewards(db_file, node_id, rewards):
    """Store rewards in the database."""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Store each reward
        for reward in rewards:
            # Check if reward already exists
            cursor.execute(
                "SELECT id FROM rewards WHERE node_id = ? AND date = ?",
                (node_id, reward['date'])
            )
            existing_reward = cursor.fetchone()
            
            if existing_reward:
                # Update existing reward
                cursor.execute(
                    """
                    UPDATE rewards
                    SET poa_points = ?, poc_points = ?, referral_points = ?, total_points = ?, created_at = ?
                    WHERE node_id = ? AND date = ?
                    """,
                    (
                        reward['poa_points'],
                        reward['poc_points'],
                        reward['referral_points'],
                        reward['total_points'],
                        datetime.now().isoformat(),
                        node_id,
                        reward['date']
                    )
                )
            else:
                # Insert new reward
                cursor.execute(
                    """
                    INSERT INTO rewards
                    (node_id, date, poa_points, poc_points, referral_points, total_points, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        node_id,
                        reward['date'],
                        reward['poa_points'],
                        reward['poc_points'],
                        reward['referral_points'],
                        reward['total_points'],
                        datetime.now().isoformat()
                    )
                )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Stored {len(rewards)} rewards for node {node_id}")
        return True
    except Exception as e:
        logger.error(f"Error storing rewards for node {node_id}: {str(e)}")
        return False

def update_daily_rewards(db_file, date):
    """Update daily rewards for a specific date."""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Calculate daily rewards
        cursor.execute(
            """
            SELECT
                SUM(poa_points) as poa_points,
                SUM(poc_points) as poc_points,
                SUM(referral_points) as referral_points,
                SUM(total_points) as total_points
            FROM rewards
            WHERE date = ?
            """,
            (date.strftime("%Y-%m-%d"),)
        )
        
        daily_rewards = cursor.fetchone()
        
        if daily_rewards and daily_rewards[0] is not None:
            # Check if daily reward already exists
            cursor.execute(
                "SELECT id FROM daily_rewards WHERE date = ?",
                (date.strftime("%Y-%m-%d"),)
            )
            existing_daily_reward = cursor.fetchone()
            
            if existing_daily_reward:
                # Update existing daily reward
                cursor.execute(
                    """
                    UPDATE daily_rewards
                    SET poa_points = ?, poc_points = ?, referral_points = ?, total_points = ?, created_at = ?
                    WHERE date = ?
                    """,
                    (
                        daily_rewards[0],
                        daily_rewards[1],
                        daily_rewards[2],
                        daily_rewards[3],
                        datetime.now().isoformat(),
                        date.strftime("%Y-%m-%d")
                    )
                )
            else:
                # Insert new daily reward
                cursor.execute(
                    """
                    INSERT INTO daily_rewards
                    (date, poa_points, poc_points, referral_points, total_points, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        date.strftime("%Y-%m-%d"),
                        daily_rewards[0],
                        daily_rewards[1],
                        daily_rewards[2],
                        daily_rewards[3],
                        datetime.now().isoformat()
                    )
                )
            
            conn.commit()
            logger.info(f"Updated daily rewards for {date.strftime('%Y-%m-%d')}")
        
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error updating daily rewards for {date.strftime('%Y-%m-%d')}: {str(e)}")
        return False

def collect_rewards(nodes_file, db_file, api_url, api_key, days=7):
    """Collect rewards for all nodes."""
    start_time = datetime.now()
    logger.info(f"Starting reward collection at {start_time}")
    
    # Initialize database
    if not initialize_database(db_file):
        logger.error("Failed to initialize database")
        return
    
    # Load nodes
    nodes = load_nodes(nodes_file)
    if not nodes:
        logger.error(f"No nodes found in {nodes_file}")
        return
    
    # Set date range
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Collect rewards for each node
    for node in nodes:
        logger.info(f"Collecting rewards for node {node['name']} ({node['id']})")
        
        # Get rewards from API
        rewards = get_rewards_from_api(api_url, api_key, node['id'], start_date, end_date)
        
        if rewards:
            # Store rewards in database
            store_rewards(db_file, node['id'], rewards)
    
    # Update daily rewards for each day in the date range
    current_date = start_date
    while current_date <= end_date:
        update_daily_rewards(db_file, current_date)
        current_date += timedelta(days=1)
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"Reward collection completed at {end_time} (duration: {duration})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect reward data from the Gradient Network")
    parser.add_argument("--nodes-file", default="nodes.json", help="Path to nodes JSON file")
    parser.add_argument("--db-file", default="rewards.db", help="Path to rewards database file")
    parser.add_argument("--api-url", required=True, help="Gradient Network API URL")
    parser.add_argument("--api-key", required=True, help="Gradient Network API key")
    parser.add_argument("--days", type=int, default=7, help="Number of days to collect rewards for")
    args = parser.parse_args()
    
    collect_rewards(args.nodes_file, args.db_file, args.api_url, args.api_key, args.days)
