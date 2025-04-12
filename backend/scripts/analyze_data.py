#!/usr/bin/env python3
"""
Script to analyze the collected data from the Gradient Network.
This script generates reports and insights from the collected data.
"""
import os
import sys
import json
import logging
import argparse
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_analysis.log"),
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

def get_rewards_data(db_file):
    """Get rewards data from the database."""
    try:
        conn = sqlite3.connect(db_file)
        
        # Get node rewards
        node_rewards = pd.read_sql_query(
            """
            SELECT
                node_id,
                date,
                poa_points,
                poc_points,
                referral_points,
                total_points
            FROM rewards
            ORDER BY date
            """,
            conn
        )
        
        # Get daily rewards
        daily_rewards = pd.read_sql_query(
            """
            SELECT
                date,
                poa_points,
                poc_points,
                referral_points,
                total_points
            FROM daily_rewards
            ORDER BY date
            """,
            conn
        )
        
        conn.close()
        
        logger.info(f"Got rewards data: {len(node_rewards)} node rewards, {len(daily_rewards)} daily rewards")
        return node_rewards, daily_rewards
    except Exception as e:
        logger.error(f"Error getting rewards data: {str(e)}")
        return None, None

def analyze_rewards_by_node(node_rewards, nodes):
    """Analyze rewards by node."""
    try:
        # Create a dictionary to map node IDs to names
        node_names = {node['id']: node['name'] for node in nodes}
        
        # Add node names to the rewards data
        node_rewards['node_name'] = node_rewards['node_id'].map(node_names)
        
        # Group by node and calculate total rewards
        node_totals = node_rewards.groupby('node_id').agg({
            'poa_points': 'sum',
            'poc_points': 'sum',
            'referral_points': 'sum',
            'total_points': 'sum'
        }).reset_index()
        
        # Add node names to the totals
        node_totals['node_name'] = node_totals['node_id'].map(node_names)
        
        # Sort by total points
        node_totals = node_totals.sort_values('total_points', ascending=False)
        
        logger.info(f"Analyzed rewards by node: {len(node_totals)} nodes")
        return node_totals
    except Exception as e:
        logger.error(f"Error analyzing rewards by node: {str(e)}")
        return None

def analyze_rewards_by_day(daily_rewards):
    """Analyze rewards by day."""
    try:
        # Convert date to datetime
        daily_rewards['date'] = pd.to_datetime(daily_rewards['date'])
        
        # Sort by date
        daily_rewards = daily_rewards.sort_values('date')
        
        # Calculate cumulative rewards
        daily_rewards['cumulative_poa'] = daily_rewards['poa_points'].cumsum()
        daily_rewards['cumulative_poc'] = daily_rewards['poc_points'].cumsum()
        daily_rewards['cumulative_referral'] = daily_rewards['referral_points'].cumsum()
        daily_rewards['cumulative_total'] = daily_rewards['total_points'].cumsum()
        
        # Calculate 7-day moving average
        daily_rewards['ma7_total'] = daily_rewards['total_points'].rolling(window=7).mean()
        
        logger.info(f"Analyzed rewards by day: {len(daily_rewards)} days")
        return daily_rewards
    except Exception as e:
        logger.error(f"Error analyzing rewards by day: {str(e)}")
        return None

def analyze_reward_types(daily_rewards):
    """Analyze reward types."""
    try:
        # Calculate total rewards by type
        total_poa = daily_rewards['poa_points'].sum()
        total_poc = daily_rewards['poc_points'].sum()
        total_referral = daily_rewards['referral_points'].sum()
        total_all = daily_rewards['total_points'].sum()
        
        # Calculate percentages
        poa_percent = (total_poa / total_all) * 100 if total_all > 0 else 0
        poc_percent = (total_poc / total_all) * 100 if total_all > 0 else 0
        referral_percent = (total_referral / total_all) * 100 if total_all > 0 else 0
        
        reward_types = {
            'poa': {
                'total': total_poa,
                'percent': poa_percent
            },
            'poc': {
                'total': total_poc,
                'percent': poc_percent
            },
            'referral': {
                'total': total_referral,
                'percent': referral_percent
            },
            'total': total_all
        }
        
        logger.info(f"Analyzed reward types: POA {poa_percent:.2f}%, POC {poc_percent:.2f}%, Referral {referral_percent:.2f}%")
        return reward_types
    except Exception as e:
        logger.error(f"Error analyzing reward types: {str(e)}")
        return None

def generate_node_performance_report(node_rewards, nodes, output_dir):
    """Generate a node performance report."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create a dictionary to map node IDs to names
        node_names = {node['id']: node['name'] for node in nodes}
        
        # Add node names to the rewards data
        node_rewards['node_name'] = node_rewards['node_id'].map(node_names)
        
        # Convert date to datetime
        node_rewards['date'] = pd.to_datetime(node_rewards['date'])
        
        # Create a report for each node
        for node in nodes:
            node_id = node['id']
            node_name = node['name']
            
            # Filter rewards for this node
            node_data = node_rewards[node_rewards['node_id'] == node_id]
            
            if len(node_data) == 0:
                logger.warning(f"No rewards data for node {node_name} ({node_id})")
                continue
            
            # Calculate total rewards
            total_poa = node_data['poa_points'].sum()
            total_poc = node_data['poc_points'].sum()
            total_referral = node_data['referral_points'].sum()
            total_all = node_data['total_points'].sum()
            
            # Calculate daily average
            daily_avg = node_data.groupby('date')['total_points'].sum().mean()
            
            # Calculate best and worst days
            daily_totals = node_data.groupby('date')['total_points'].sum()
            best_day = daily_totals.idxmax() if len(daily_totals) > 0 else None
            best_day_points = daily_totals.max() if len(daily_totals) > 0 else 0
            worst_day = daily_totals.idxmin() if len(daily_totals) > 0 else None
            worst_day_points = daily_totals.min() if len(daily_totals) > 0 else 0
            
            # Create report
            report = {
                'node_id': node_id,
                'node_name': node_name,
                'total_rewards': {
                    'poa': total_poa,
                    'poc': total_poc,
                    'referral': total_referral,
                    'total': total_all
                },
                'daily_average': daily_avg,
                'best_day': {
                    'date': best_day.strftime('%Y-%m-%d') if best_day else None,
                    'points': best_day_points
                },
                'worst_day': {
                    'date': worst_day.strftime('%Y-%m-%d') if worst_day else None,
                    'points': worst_day_points
                }
            }
            
            # Save report to file
            report_file = os.path.join(output_dir, f"node_{node_id}_report.json")
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Generated performance report for node {node_name} ({node_id})")
            
            # Create a plot of daily rewards
            plt.figure(figsize=(12, 6))
            
            # Group by date and plot
            daily_data = node_data.groupby('date').agg({
                'poa_points': 'sum',
                'poc_points': 'sum',
                'referral_points': 'sum',
                'total_points': 'sum'
            })
            
            daily_data.plot(kind='bar', stacked=True, ax=plt.gca())
            
            plt.title(f"Daily Rewards for {node_name}")
            plt.xlabel("Date")
            plt.ylabel("Points")
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save plot to file
            plot_file = os.path.join(output_dir, f"node_{node_id}_daily_rewards.png")
            plt.savefig(plot_file)
            plt.close()
        
        logger.info(f"Generated node performance reports for {len(nodes)} nodes")
        return True
    except Exception as e:
        logger.error(f"Error generating node performance report: {str(e)}")
        return False

def generate_overall_performance_report(daily_rewards, reward_types, output_dir):
    """Generate an overall performance report."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Calculate key metrics
        total_days = len(daily_rewards)
        total_rewards = reward_types['total']
        daily_average = total_rewards / total_days if total_days > 0 else 0
        
        # Calculate best and worst days
        best_day = daily_rewards.loc[daily_rewards['total_points'].idxmax()] if len(daily_rewards) > 0 else None
        worst_day = daily_rewards.loc[daily_rewards['total_points'].idxmin()] if len(daily_rewards) > 0 else None
        
        # Create report
        report = {
            'total_days': total_days,
            'total_rewards': total_rewards,
            'daily_average': daily_average,
            'reward_types': reward_types,
            'best_day': {
                'date': best_day['date'].strftime('%Y-%m-%d') if best_day is not None else None,
                'points': best_day['total_points'] if best_day is not None else 0
            },
            'worst_day': {
                'date': worst_day['date'].strftime('%Y-%m-%d') if worst_day is not None else None,
                'points': worst_day['total_points'] if worst_day is not None else 0
            }
        }
        
        # Save report to file
        report_file = os.path.join(output_dir, "overall_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Generated overall performance report")
        
        # Create a plot of daily rewards
        plt.figure(figsize=(12, 6))
        
        # Plot daily rewards
        plt.bar(daily_rewards['date'], daily_rewards['total_points'])
        plt.plot(daily_rewards['date'], daily_rewards['ma7_total'], 'r-', label='7-day MA')
        
        plt.title("Daily Rewards")
        plt.xlabel("Date")
        plt.ylabel("Points")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save plot to file
        plot_file = os.path.join(output_dir, "daily_rewards.png")
        plt.savefig(plot_file)
        plt.close()
        
        # Create a plot of reward types
        plt.figure(figsize=(8, 8))
        
        # Plot reward types
        plt.pie(
            [reward_types['poa']['total'], reward_types['poc']['total'], reward_types['referral']['total']],
            labels=['POA', 'POC', 'Referral'],
            autopct='%1.1f%%',
            startangle=90
        )
        
        plt.title("Reward Types")
        plt.axis('equal')
        
        # Save plot to file
        plot_file = os.path.join(output_dir, "reward_types.png")
        plt.savefig(plot_file)
        plt.close()
        
        # Create a plot of cumulative rewards
        plt.figure(figsize=(12, 6))
        
        # Plot cumulative rewards
        plt.plot(daily_rewards['date'], daily_rewards['cumulative_total'], label='Total')
        plt.plot(daily_rewards['date'], daily_rewards['cumulative_poa'], label='POA')
        plt.plot(daily_rewards['date'], daily_rewards['cumulative_poc'], label='POC')
        plt.plot(daily_rewards['date'], daily_rewards['cumulative_referral'], label='Referral')
        
        plt.title("Cumulative Rewards")
        plt.xlabel("Date")
        plt.ylabel("Points")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        # Save plot to file
        plot_file = os.path.join(output_dir, "cumulative_rewards.png")
        plt.savefig(plot_file)
        plt.close()
        
        return True
    except Exception as e:
        logger.error(f"Error generating overall performance report: {str(e)}")
        return False

def analyze_data(nodes_file, db_file, output_dir):
    """Analyze the collected data and generate reports."""
    start_time = datetime.now()
    logger.info(f"Starting data analysis at {start_time}")
    
    # Load nodes
    nodes = load_nodes(nodes_file)
    if not nodes:
        logger.error(f"No nodes found in {nodes_file}")
        return
    
    # Get rewards data
    node_rewards, daily_rewards = get_rewards_data(db_file)
    if node_rewards is None or daily_rewards is None:
        logger.error("Failed to get rewards data")
        return
    
    # Analyze rewards by node
    node_totals = analyze_rewards_by_node(node_rewards, nodes)
    if node_totals is None:
        logger.error("Failed to analyze rewards by node")
        return
    
    # Analyze rewards by day
    daily_rewards = analyze_rewards_by_day(daily_rewards)
    if daily_rewards is None:
        logger.error("Failed to analyze rewards by day")
        return
    
    # Analyze reward types
    reward_types = analyze_reward_types(daily_rewards)
    if reward_types is None:
        logger.error("Failed to analyze reward types")
        return
    
    # Generate node performance report
    if not generate_node_performance_report(node_rewards, nodes, output_dir):
        logger.error("Failed to generate node performance report")
        return
    
    # Generate overall performance report
    if not generate_overall_performance_report(daily_rewards, reward_types, output_dir):
        logger.error("Failed to generate overall performance report")
        return
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"Data analysis completed at {end_time} (duration: {duration})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze the collected data from the Gradient Network")
    parser.add_argument("--nodes-file", default="nodes.json", help="Path to nodes JSON file")
    parser.add_argument("--db-file", default="rewards.db", help="Path to rewards database file")
    parser.add_argument("--output-dir", default="reports", help="Path to output directory for reports")
    args = parser.parse_args()
    
    analyze_data(args.nodes_file, args.db_file, args.output_dir)
