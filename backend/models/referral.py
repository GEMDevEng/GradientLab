"""
Referral model for node referrals.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base, get_session
import logging

logger = logging.getLogger(__name__)

class Referral(Base):
    """Referral model for node referrals."""
    __tablename__ = 'referrals'
    
    id = Column(Integer, primary_key=True)
    referrer_node_id = Column(Integer, ForeignKey('nodes.id'))
    referred_node_id = Column(Integer, ForeignKey('nodes.id'))
    bonus_percentage = Column(Float, default=10.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    referrer_node = relationship('Node', foreign_keys=[referrer_node_id], back_populates='referrals_as_referrer')
    referred_node = relationship('Node', foreign_keys=[referred_node_id], back_populates='referrals_as_referred')
    
    def to_dict(self):
        """Convert Referral to dictionary."""
        return {
            'id': self.id,
            'referrer_node_id': self.referrer_node_id,
            'referred_node_id': self.referred_node_id,
            'bonus_percentage': self.bonus_percentage,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

def get_referral_by_id(referral_id):
    """Get a Referral by ID."""
    session = get_session()
    try:
        return session.query(Referral).filter(Referral.id == referral_id).first()
    except Exception as e:
        logger.error(f"Error getting Referral by ID: {str(e)}")
        return None
    finally:
        session.close()

def get_referrals_by_referrer(node_id):
    """Get all Referrals where the node is the referrer."""
    session = get_session()
    try:
        return session.query(Referral).filter(Referral.referrer_node_id == node_id).all()
    except Exception as e:
        logger.error(f"Error getting Referrals by referrer: {str(e)}")
        return []
    finally:
        session.close()

def get_referrals_by_referred(node_id):
    """Get all Referrals where the node is the referred."""
    session = get_session()
    try:
        return session.query(Referral).filter(Referral.referred_node_id == node_id).all()
    except Exception as e:
        logger.error(f"Error getting Referrals by referred: {str(e)}")
        return []
    finally:
        session.close()

def create_referral(referrer_node_id, referred_node_id, bonus_percentage=10.0):
    """Create a new Referral."""
    session = get_session()
    try:
        # Check if a referral already exists
        existing_referral = session.query(Referral).filter(
            Referral.referrer_node_id == referrer_node_id,
            Referral.referred_node_id == referred_node_id
        ).first()
        
        if existing_referral:
            return None
        
        # Check if the node is trying to refer itself
        if referrer_node_id == referred_node_id:
            return None
        
        # Create new referral
        referral = Referral(
            referrer_node_id=referrer_node_id,
            referred_node_id=referred_node_id,
            bonus_percentage=bonus_percentage
        )
        session.add(referral)
        session.commit()
        return referral
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating Referral: {str(e)}")
        return None
    finally:
        session.close()

def update_referral(referral_id, **kwargs):
    """Update a Referral."""
    session = get_session()
    try:
        referral = session.query(Referral).filter(Referral.id == referral_id).first()
        if not referral:
            return None
        
        for key, value in kwargs.items():
            if hasattr(referral, key):
                setattr(referral, key, value)
        
        session.commit()
        return referral
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating Referral: {str(e)}")
        return None
    finally:
        session.close()

def delete_referral(referral_id):
    """Delete a Referral."""
    session = get_session()
    try:
        referral = session.query(Referral).filter(Referral.id == referral_id).first()
        if not referral:
            return False
        
        session.delete(referral)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting Referral: {str(e)}")
        return False
    finally:
        session.close()
