"""
Tests for the two-factor authentication API.
"""
import json
import pytest
import pyotp

def test_2fa_setup(client, auth_token):
    """Test setting up two-factor authentication."""
    response = client.post('/api/2fa/setup', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'secret' in data['data']
    assert 'uri' in data['data']

def test_2fa_verify_valid_code(client, auth_token):
    """Test verifying a valid two-factor authentication code."""
    # First, set up 2FA
    setup_response = client.post('/api/2fa/setup', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    setup_data = json.loads(setup_response.data)
    secret = setup_data['data']['secret']
    
    # Generate a valid OTP code
    totp = pyotp.TOTP(secret)
    valid_code = totp.now()
    
    # Verify the code
    response = client.post('/api/2fa/verify', json={
        'code': valid_code
    }, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'backup_codes' in data['data']

def test_2fa_verify_invalid_code(client, auth_token):
    """Test verifying an invalid two-factor authentication code."""
    # First, set up 2FA
    client.post('/api/2fa/setup', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    
    # Use an invalid code
    response = client.post('/api/2fa/verify', json={
        'code': '000000'
    }, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'Invalid verification code' in data['message']

def test_2fa_status(client, auth_token):
    """Test getting two-factor authentication status."""
    response = client.get('/api/2fa/status', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'enabled' in data['data']
    assert 'verified' in data['data']
    assert 'has_backup_codes' in data['data']

def test_2fa_disable(client, auth_token):
    """Test disabling two-factor authentication."""
    # First, set up and verify 2FA
    setup_response = client.post('/api/2fa/setup', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    setup_data = json.loads(setup_response.data)
    secret = setup_data['data']['secret']
    
    # Generate a valid OTP code
    totp = pyotp.TOTP(secret)
    valid_code = totp.now()
    
    # Verify the code
    client.post('/api/2fa/verify', json={
        'code': valid_code
    }, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    
    # Now disable 2FA
    response = client.post('/api/2fa/disable', json={
        'code': valid_code
    }, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'Two-factor authentication disabled' in data['message']
    
    # Check that 2FA is disabled
    status_response = client.get('/api/2fa/status', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    status_data = json.loads(status_response.data)
    assert status_data['data']['enabled'] is False
