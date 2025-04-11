"""
Tests for Data Collection API endpoints.
"""
import unittest
import json
from app import app

class TestDataCollectionAPI(unittest.TestCase):
    """Test cases for Data Collection API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_rewards_empty(self):
        """Test getting rewards when none exist."""
        response = self.app.get('/api/data/rewards')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']), 0)

    def test_create_reward(self):
        """Test creating a new reward record."""
        reward_data = {
            'node_id': 1,
            'poa_points': 25,
            'poc_points': 15,
            'referral_points': 10,
            'date': '2023-04-14'
        }
        
        response = self.app.post('/api/data/rewards', 
                                json=reward_data,
                                content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['node_id'], 1)
        self.assertEqual(data['data']['poa_points'], 25)
        self.assertEqual(data['data']['poc_points'], 15)
        self.assertEqual(data['data']['referral_points'], 10)
        self.assertEqual(data['data']['date'], '2023-04-14')

    def test_get_node_rewards(self):
        """Test getting rewards for a specific node."""
        # First create rewards for two different nodes
        reward_data_1 = {
            'node_id': 1,
            'poa_points': 25,
            'poc_points': 15,
            'referral_points': 10,
            'date': '2023-04-14'
        }
        
        reward_data_2 = {
            'node_id': 2,
            'poa_points': 30,
            'poc_points': 20,
            'referral_points': 5,
            'date': '2023-04-14'
        }
        
        self.app.post('/api/data/rewards', 
                     json=reward_data_1,
                     content_type='application/json')
        
        self.app.post('/api/data/rewards', 
                     json=reward_data_2,
                     content_type='application/json')
        
        # Now get rewards for node 1
        response = self.app.get('/api/data/rewards/node/1')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['node_id'], 1)
        self.assertEqual(data['data'][0]['poa_points'], 25)
        self.assertEqual(data['data'][0]['poc_points'], 15)
        self.assertEqual(data['data'][0]['referral_points'], 10)

    def test_simulate_rewards(self):
        """Test simulating rewards for a node."""
        response = self.app.post('/api/data/rewards/simulate/1', 
                                json={'days': 5},
                                content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']), 5)
        
        # Check that all rewards are for node 1
        for reward in data['data']:
            self.assertEqual(reward['node_id'], 1)
            self.assertTrue('poa_points' in reward)
            self.assertTrue('poc_points' in reward)
            self.assertTrue('referral_points' in reward)
            self.assertTrue('date' in reward)

    def test_get_reward_stats(self):
        """Test getting reward statistics."""
        # First create some rewards
        reward_data_1 = {
            'node_id': 1,
            'poa_points': 25,
            'poc_points': 15,
            'referral_points': 10,
            'date': '2023-04-14'
        }
        
        reward_data_2 = {
            'node_id': 2,
            'poa_points': 30,
            'poc_points': 20,
            'referral_points': 5,
            'date': '2023-04-14'
        }
        
        self.app.post('/api/data/rewards', 
                     json=reward_data_1,
                     content_type='application/json')
        
        self.app.post('/api/data/rewards', 
                     json=reward_data_2,
                     content_type='application/json')
        
        # Now get reward stats
        response = self.app.get('/api/data/rewards/stats')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['total_poa_points'], 55)
        self.assertEqual(data['data']['total_poc_points'], 35)
        self.assertEqual(data['data']['total_referral_points'], 15)
        self.assertEqual(data['data']['total_points'], 105)
        self.assertEqual(data['data']['nodes_count'], 2)
        self.assertEqual(data['data']['average_points_per_node'], 52.5)

if __name__ == '__main__':
    unittest.main()
