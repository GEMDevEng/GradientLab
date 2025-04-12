"""
Test configuration for GradientLab backend.
"""
import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the path so we can import from the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from config.database import Base, get_session
from models.user import User

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Set test configuration
    flask_app.config.update({
        'TESTING': True,
        'JWT_SECRET_KEY': 'test_secret_key',
        'DATABASE_URL': 'sqlite:///:memory:',
    })

    # Create the database and tables
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    
    # Create a session factory
    session_factory = sessionmaker(bind=engine)
    
    # Override the get_session function to use the test session
    def _get_test_session():
        return session_factory()
    
    # Patch the get_session function
    import config.database
    config.database.get_session = _get_test_session
    
    # Create a test user
    with _get_test_session() as session:
        test_user = User(
            username='testuser',
            email='test@example.com',
            role='admin'
        )
        test_user.set_password('password123')
        session.add(test_user)
        session.commit()
    
    yield flask_app
    
    # Clean up
    Base.metadata.drop_all(engine)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def auth_token(client):
    """Get an authentication token for the test user."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    return response.json['data']['access_token']
