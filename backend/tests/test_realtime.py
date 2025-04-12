"""
Tests for Real-time API endpoints.
"""
import json
import pytest
from unittest.mock import patch

def test_get_realtime_status(client, auth_token):
    """Test getting real-time status."""
    response = client.get('/api/realtime/status', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'connection_status' in data['data']
    assert 'last_update' in data['data']
    assert 'active_nodes' in data['data']
    assert 'recent_rewards' in data['data']

@patch('api.realtime.emit_status_update')
def test_trigger_status_update(mock_emit, client, auth_token):
    """Test triggering a status update."""
    response = client.post('/api/realtime/update', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'message' in data
    
    # Check that emit_status_update was called
    mock_emit.assert_called_once()

def test_get_active_connections(client, auth_token):
    """Test getting active connections."""
    response = client.get('/api/realtime/connections', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'count' in data['data']
    assert 'connections' in data['data']

@patch('api.realtime.broadcast_message')
def test_send_broadcast(mock_broadcast, client, auth_token):
    """Test sending a broadcast message."""
    response = client.post('/api/realtime/broadcast', json={
        'message': 'Test broadcast message',
        'type': 'info'
    }, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'message' in data
    
    # Check that broadcast_message was called with the right arguments
    mock_broadcast.assert_called_once_with('Test broadcast message', 'info')

def test_get_event_history(client, auth_token):
    """Test getting event history."""
    response = client.get('/api/realtime/events', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'events' in data['data']
    
    # Events should be a list
    assert isinstance(data['data']['events'], list)
