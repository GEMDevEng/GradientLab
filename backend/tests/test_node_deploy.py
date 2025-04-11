"""
Tests for Node deployment API endpoints.
"""
import unittest
import json
from app import app

class TestNodeDeployAPI(unittest.TestCase):
    """Test cases for Node deployment API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_nodes_empty(self):
        """Test getting nodes when none exist."""
        response = self.app.get('/api/node/nodes')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']), 0)

    def test_create_node(self):
        """Test creating a new node."""
        node_data = {
            'vm_id': 1
        }
        
        response = self.app.post('/api/node/nodes', 
                                json=node_data,
                                content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['vm_id'], 1)
        self.assertEqual(data['data']['status'], 'deploying')
        self.assertEqual(data['data']['uptime_percentage'], 0.0)

    def test_get_node_by_id(self):
        """Test getting a node by ID."""
        # First create a node
        node_data = {
            'vm_id': 1
        }
        
        create_response = self.app.post('/api/node/nodes', 
                                      json=node_data,
                                      content_type='application/json')
        create_data = json.loads(create_response.data)
        node_id = create_data['data']['id']
        
        # Now get the node by ID
        response = self.app.get(f'/api/node/nodes/{node_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], node_id)
        self.assertEqual(data['data']['vm_id'], 1)
        self.assertEqual(data['data']['status'], 'deploying')

    def test_update_node(self):
        """Test updating a node."""
        # First create a node
        node_data = {
            'vm_id': 1
        }
        
        create_response = self.app.post('/api/node/nodes', 
                                      json=node_data,
                                      content_type='application/json')
        create_data = json.loads(create_response.data)
        node_id = create_data['data']['id']
        
        # Now update the node
        update_data = {
            'status': 'running',
            'uptime_percentage': 95.5
        }
        
        response = self.app.put(f'/api/node/nodes/{node_id}', 
                              json=update_data,
                              content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], node_id)
        self.assertEqual(data['data']['status'], 'running')
        self.assertEqual(data['data']['uptime_percentage'], 95.5)
        self.assertEqual(data['data']['vm_id'], 1)  # Unchanged

    def test_delete_node(self):
        """Test deleting a node."""
        # First create a node
        node_data = {
            'vm_id': 1
        }
        
        create_response = self.app.post('/api/node/nodes', 
                                      json=node_data,
                                      content_type='application/json')
        create_data = json.loads(create_response.data)
        node_id = create_data['data']['id']
        
        # Now delete the node
        response = self.app.delete(f'/api/node/nodes/{node_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], node_id)
        
        # Verify the node is deleted
        get_response = self.app.get(f'/api/node/nodes/{node_id}')
        get_data = json.loads(get_response.data)
        
        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(get_data['status'], 'error')

    def test_start_node(self):
        """Test starting a node."""
        # First create a node
        node_data = {
            'vm_id': 1
        }
        
        create_response = self.app.post('/api/node/nodes', 
                                      json=node_data,
                                      content_type='application/json')
        create_data = json.loads(create_response.data)
        node_id = create_data['data']['id']
        
        # Now start the node
        response = self.app.post(f'/api/node/nodes/{node_id}/start')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], node_id)
        self.assertEqual(data['data']['status'], 'running')

    def test_stop_node(self):
        """Test stopping a node."""
        # First create a node and start it
        node_data = {
            'vm_id': 1
        }
        
        create_response = self.app.post('/api/node/nodes', 
                                      json=node_data,
                                      content_type='application/json')
        create_data = json.loads(create_response.data)
        node_id = create_data['data']['id']
        
        self.app.post(f'/api/node/nodes/{node_id}/start')
        
        # Now stop the node
        response = self.app.post(f'/api/node/nodes/{node_id}/stop')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], node_id)
        self.assertEqual(data['data']['status'], 'stopped')

if __name__ == '__main__':
    unittest.main()
