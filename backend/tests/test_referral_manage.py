"""
Tests for Referral Management API endpoints.
"""
import json
import pytest
from unittest.mock import patch

def test_get_referrals_empty(client, auth_token):
    """Test getting referrals when none exist."""
    response = client.get('/api/referral', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert len(data['data']) == 0

def test_generate_referral(client, auth_token):
    """Test generating a new referral link."""
    response = client.post('/api/referral', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'code' in data['data']
    assert 'url' in data['data']
    assert 'created_at' in data['data']
    assert data['data']['used_count'] == 0
    assert data['data']['is_active'] is True

def test_get_referral_by_code(client, auth_token):
    """Test getting a referral by code."""
    # First generate a referral
    create_response = client.post('/api/referral', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    create_data = json.loads(create_response.data)
    code = create_data['data']['code']
    
    # Now get the referral by code
    response = client.get(f'/api/referral/{code}', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['code'] == code
    assert data['data']['used_count'] == 0
    assert data['data']['is_active'] is True

def test_deactivate_referral(client, auth_token):
    """Test deactivating a referral."""
    # First generate a referral
    create_response = client.post('/api/referral', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    create_data = json.loads(create_response.data)
    code = create_data['data']['code']
    
    # Now deactivate the referral
    response = client.put(f'/api/referral/{code}/deactivate', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['code'] == code
    assert data['data']['is_active'] is False
    
    # Verify the referral is deactivated
    get_response = client.get(f'/api/referral/{code}', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    get_data = json.loads(get_response.data)
    assert get_data['data']['is_active'] is False

def test_reactivate_referral(client, auth_token):
    """Test reactivating a referral."""
    # First generate a referral
    create_response = client.post('/api/referral', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    create_data = json.loads(create_response.data)
    code = create_data['data']['code']
    
    # Deactivate the referral
    client.put(f'/api/referral/{code}/deactivate', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    
    # Now reactivate the referral
    response = client.put(f'/api/referral/{code}/activate', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['code'] == code
    assert data['data']['is_active'] is True
    
    # Verify the referral is reactivated
    get_response = client.get(f'/api/referral/{code}', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    get_data = json.loads(get_response.data)
    assert get_data['data']['is_active'] is True

def test_track_referral_use(client, auth_token):
    """Test tracking referral use."""
    # First generate a referral
    create_response = client.post('/api/referral', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    create_data = json.loads(create_response.data)
    code = create_data['data']['code']
    
    # Now track a use of the referral
    response = client.post(f'/api/referral/{code}/track', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['code'] == code
    assert data['data']['used_count'] == 1
    
    # Track another use
    response = client.post(f'/api/referral/{code}/track', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['used_count'] == 2

def test_get_referral_stats(client, auth_token):
    """Test getting referral statistics."""
    # First generate some referrals and track uses
    for _ in range(3):
        create_response = client.post('/api/referral', headers={
            'Authorization': f'Bearer {auth_token}'
        })
        create_data = json.loads(create_response.data)
        code = create_data['data']['code']
        
        # Track uses for this referral
        for _ in range(2):
            client.post(f'/api/referral/{code}/track', headers={
                'Authorization': f'Bearer {auth_token}'
            })
    
    # Now get referral stats
    response = client.get('/api/referral/stats', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['total_referrals'] == 3
    assert data['data']['total_uses'] == 6
    assert data['data']['average_uses_per_referral'] == 2.0
