"""
User model for authentication.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256
from config.database import Base, get_session
import logging

logger = logging.getLogger(__name__)

class User(Base):
    """User model for authentication."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='user')
    name = Column(String(100))
    bio = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    vms = relationship('VM', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, username, email, password, role='user', name=None, bio=None):
        """Initialize a new user."""
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role
        self.name = name
        self.bio = bio

    def set_password(self, password):
        """Set the user's password."""
        self.password_hash = pbkdf2_sha256.hash(password)

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
            'name': self.name,
            'bio': self.bio,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def get_user_by_username(username):
    """Get a user by username."""
    session = get_session()
    try:
        return session.query(User).filter(User.username == username).first()
    except Exception as e:
        logger.error(f"Error getting user by username: {str(e)}")
        return None
    finally:
        session.close()

def get_user_by_id(user_id):
    """Get a user by ID."""
    session = get_session()
    try:
        return session.query(User).filter(User.id == user_id).first()
    except Exception as e:
        logger.error(f"Error getting user by ID: {str(e)}")
        return None
    finally:
        session.close()

def create_user(username, email, password, role='user', name=None, bio=None):
    """Create a new user."""
    session = get_session()
    try:
        # Check if username already exists
        if session.query(User).filter(User.username == username).first():
            return None

        # Create new user
        user = User(username, email, password, role, name, bio)
        session.add(user)
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating user: {str(e)}")
        return None
    finally:
        session.close()

def create_admin_user():
    """Create a default admin user if it doesn't exist."""
    session = get_session()
    try:
        # Check if admin user already exists
        admin = session.query(User).filter(User.username == 'admin').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@gradientlab.com',
                password='admin123',
                role='admin',
                name='Admin User'
            )
            session.add(admin)
            session.commit()
            logger.info("Default admin user created")
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating admin user: {str(e)}")
    finally:
        session.close()
