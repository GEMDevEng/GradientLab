"""
Tests for the authentication API.
"""
import json
import pytest

def test_login_success(client):
    """Test successful login."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'access_token' in data['data']
    assert data['data']['user']['username'] == 'testuser'

def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'Invalid username or password' in data['message']

def test_login_missing_fields(client):
    """Test login with missing fields."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'Missing required field' in data['message']

def test_register_success(client):
    """Test successful registration."""
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'User registered successfully' in data['message']

def test_register_existing_username(client):
    """Test registration with existing username."""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'another@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'Username already exists' in data['message']

def test_register_password_mismatch(client):
    """Test registration with password mismatch."""
    response = client.post('/api/auth/register', json={
        'username': 'newuser2',
        'email': 'new2@example.com',
        'password': 'password123',
        'confirm_password': 'password456'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'Passwords do not match' in data['message']

def test_get_user_authenticated(client, auth_token):
    """Test getting user information when authenticated."""
    response = client.get('/api/auth/user', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['username'] == 'testuser'

def test_get_user_unauthenticated(client):
    """Test getting user information when not authenticated."""
    response = client.get('/api/auth/user')
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'Missing Authorization Header' in data['message']
