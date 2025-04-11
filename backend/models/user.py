"""
User model for authentication.
"""
from datetime import datetime
from passlib.hash import pbkdf2_sha256

# Mock database for users (will be replaced with SQLAlchemy)
users_db = []

class User:
    """User model for authentication."""
    
    def __init__(self, username, email, password, role='user'):
        """Initialize a new user."""
        self.id = len(users_db) + 1
        self.username = username
        self.email = email
        self.password_hash = pbkdf2_sha256.hash(password)
        self.role = role
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def verify_password(self, password):
        """Verify the user's password."""
        return pbkdf2_sha256.verify(password, self.password_hash)
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# Create a default admin user
admin_user = User(
    username='admin',
    email='admin@gradientlab.com',
    password='admin123',
    role='admin'
)
users_db.append(admin_user)

def get_user_by_username(username):
    """Get a user by username."""
    for user in users_db:
        if user.username == username:
            return user
    return None

def get_user_by_id(user_id):
    """Get a user by ID."""
    for user in users_db:
        if user.id == user_id:
            return user
    return None

def create_user(username, email, password, role='user'):
    """Create a new user."""
    # Check if username already exists
    if get_user_by_username(username):
        return None
    
    # Create new user
    user = User(username, email, password, role)
    users_db.append(user)
    return user
