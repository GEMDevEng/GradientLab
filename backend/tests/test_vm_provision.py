"""
Tests for VM provisioning API endpoints.
"""
import unittest
import json
from app import app

class TestVMProvisionAPI(unittest.TestCase):
    """Test cases for VM provisioning API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_vms_empty(self):
        """Test getting VMs when none exist."""
        response = self.app.get('/api/vm/vms')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']), 0)

    def test_create_vm(self):
        """Test creating a new VM."""
        vm_data = {
            'provider': 'oracle',
            'region': 'us-west-1',
            'name': 'test-vm'
        }
        
        response = self.app.post('/api/vm/vms', 
                                json=vm_data,
                                content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['provider'], 'oracle')
        self.assertEqual(data['data']['region'], 'us-west-1')
        self.assertEqual(data['data']['name'], 'test-vm')
        self.assertEqual(data['data']['status'], 'provisioning')

    def test_get_vm_by_id(self):
        """Test getting a VM by ID."""
        # First create a VM
        vm_data = {
            'provider': 'oracle',
            'region': 'us-west-1',
            'name': 'test-vm'
        }
        
        create_response = self.app.post('/api/vm/vms', 
                                      json=vm_data,
                                      content_type='application/json')
        create_data = json.loads(create_response.data)
        vm_id = create_data['data']['id']
        
        # Now get the VM by ID
        response = self.app.get(f'/api/vm/vms/{vm_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], vm_id)
        self.assertEqual(data['data']['provider'], 'oracle')
        self.assertEqual(data['data']['region'], 'us-west-1')
        self.assertEqual(data['data']['name'], 'test-vm')

    def test_update_vm(self):
        """Test updating a VM."""
        # First create a VM
        vm_data = {
            'provider': 'oracle',
            'region': 'us-west-1',
            'name': 'test-vm'
        }
        
        create_response = self.app.post('/api/vm/vms', 
                                      json=vm_data,
                                      content_type='application/json')
        create_data = json.loads(create_response.data)
        vm_id = create_data['data']['id']
        
        # Now update the VM
        update_data = {
            'name': 'updated-vm',
            'status': 'running'
        }
        
        response = self.app.put(f'/api/vm/vms/{vm_id}', 
                              json=update_data,
                              content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], vm_id)
        self.assertEqual(data['data']['name'], 'updated-vm')
        self.assertEqual(data['data']['status'], 'running')
        self.assertEqual(data['data']['provider'], 'oracle')  # Unchanged
        self.assertEqual(data['data']['region'], 'us-west-1')  # Unchanged

    def test_delete_vm(self):
        """Test deleting a VM."""
        # First create a VM
        vm_data = {
            'provider': 'oracle',
            'region': 'us-west-1',
            'name': 'test-vm'
        }
        
        create_response = self.app.post('/api/vm/vms', 
                                      json=vm_data,
                                      content_type='application/json')
        create_data = json.loads(create_response.data)
        vm_id = create_data['data']['id']
        
        # Now delete the VM
        response = self.app.delete(f'/api/vm/vms/{vm_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], vm_id)
        
        # Verify the VM is deleted
        get_response = self.app.get(f'/api/vm/vms/{vm_id}')
        get_data = json.loads(get_response.data)
        
        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(get_data['status'], 'error')

    def test_get_providers(self):
        """Test getting cloud providers."""
        response = self.app.get('/api/vm/providers')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(len(data['data']) > 0)
        
        # Check if Oracle Cloud is in the providers list
        oracle_provider = next((p for p in data['data'] if p['id'] == 'oracle'), None)
        self.assertIsNotNone(oracle_provider)
        self.assertEqual(oracle_provider['name'], 'Oracle Cloud')

if __name__ == '__main__':
    unittest.main()
