"""
Script to create database tables.
"""
import os
import sys
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import init_db
from models.user import create_admin_user

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Create database tables and initialize data."""
    try:
        # Initialize database tables
        init_db()
        logger.info("Database tables created successfully")
        
        # Create default admin user
        create_admin_user()
        logger.info("Default admin user created successfully")
        
        return 0
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
