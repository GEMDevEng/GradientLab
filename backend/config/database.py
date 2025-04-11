"""
Database configuration for GradientLab backend.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import logging

logger = logging.getLogger(__name__)

# Get database URL from environment variable or use default
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///gradientlab.db')

# Fix for Heroku PostgreSQL URL
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=os.environ.get('SQLALCHEMY_ECHO', 'False').lower() == 'true',
    pool_pre_ping=True
)

# Create session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Create base class for models
Base = declarative_base()

def init_db():
    """Initialize the database."""
    try:
        # Import all models to ensure they are registered with Base
        from models.user import User
        from models.vm import VM
        from models.node import Node
        from models.reward import Reward
        from models.referral import Referral
        
        # Create tables
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def get_session():
    """Get a database session."""
    return Session()

def close_session(session):
    """Close a database session."""
    session.close()
