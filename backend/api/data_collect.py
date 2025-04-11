"""
Data Collection API endpoints.
This module handles the collection and retrieval of reward data from Sentry Nodes.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import random

# Create a Blueprint for data collection
data_collect_bp = Blueprint('data_collect', __name__)

# Mock data for development (will be replaced with actual database)
mock_rewards = []

@data_collect_bp.route('/rewards', methods=['GET'])
def get_rewards():
    """Get all rewards."""
    return jsonify({
        'status': 'success',
        'data': mock_rewards
    }), 200

@data_collect_bp.route('/rewards/node/<int:node_id>', methods=['GET'])
def get_node_rewards(node_id):
    """Get rewards for a specific node."""
    node_rewards = [reward for reward in mock_rewards if reward['node_id'] == node_id]
    
    return jsonify({
        'status': 'success',
        'data': node_rewards
    }), 200

@data_collect_bp.route('/rewards', methods=['POST'])
def create_reward():
    """Record new reward data."""
    data = request.json
    
    # Validate required fields
    required_fields = ['node_id', 'poa_points', 'poc_points', 'referral_points', 'date']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Create a new reward record (mock implementation)
    new_reward = {
        'id': len(mock_rewards) + 1,
        'node_id': data['node_id'],
        'poa_points': data['poa_points'],
        'poc_points': data['poc_points'],
        'referral_points': data['referral_points'],
        'date': data['date'],
        'created_at': datetime.now().isoformat()
    }
    
    mock_rewards.append(new_reward)
    
    return jsonify({
        'status': 'success',
        'message': 'Reward data recorded successfully',
        'data': new_reward
    }), 201

@data_collect_bp.route('/rewards/simulate/<int:node_id>', methods=['POST'])
def simulate_rewards(node_id):
    """Simulate reward data for a node over a period of time."""
    data = request.json
    
    # Default to 7 days if not specified
    days = data.get('days', 7)
    
    # Generate simulated reward data
    simulated_rewards = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        
        # Simulate random reward points
        reward = {
            'id': len(mock_rewards) + i + 1,
            'node_id': node_id,
            'poa_points': random.randint(10, 50),  # Random POA points
            'poc_points': random.randint(5, 30),   # Random POC points
            'referral_points': random.randint(0, 20),  # Random referral points
            'date': date,
            'created_at': datetime.now().isoformat()
        }
        
        simulated_rewards.append(reward)
    
    # Add simulated rewards to mock data
    mock_rewards.extend(simulated_rewards)
    
    return jsonify({
        'status': 'success',
        'message': f'Simulated {days} days of reward data for node {node_id}',
        'data': simulated_rewards
    }), 201

@data_collect_bp.route('/rewards/stats', methods=['GET'])
def get_reward_stats():
    """Get aggregated reward statistics."""
    if not mock_rewards:
        return jsonify({
            'status': 'success',
            'data': {
                'total_poa_points': 0,
                'total_poc_points': 0,
                'total_referral_points': 0,
                'total_points': 0,
                'nodes_count': 0,
                'average_points_per_node': 0
            }
        }), 200
    
    # Calculate statistics
    total_poa_points = sum(reward['poa_points'] for reward in mock_rewards)
    total_poc_points = sum(reward['poc_points'] for reward in mock_rewards)
    total_referral_points = sum(reward['referral_points'] for reward in mock_rewards)
    total_points = total_poa_points + total_poc_points + total_referral_points
    
    # Get unique node IDs
    node_ids = set(reward['node_id'] for reward in mock_rewards)
    nodes_count = len(node_ids)
    
    # Calculate average points per node
    average_points_per_node = total_points / nodes_count if nodes_count > 0 else 0
    
    return jsonify({
        'status': 'success',
        'data': {
            'total_poa_points': total_poa_points,
            'total_poc_points': total_poc_points,
            'total_referral_points': total_referral_points,
            'total_points': total_points,
            'nodes_count': nodes_count,
            'average_points_per_node': average_points_per_node
        }
    }), 200
