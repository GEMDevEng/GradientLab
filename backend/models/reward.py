"""
Reward model for node rewards.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base, get_session
import logging

logger = logging.getLogger(__name__)

class Reward(Base):
    """Reward model for node rewards."""
    __tablename__ = 'rewards'
    
    id = Column(Integer, primary_key=True)
    node_id = Column(Integer, ForeignKey('nodes.id'))
    poa_points = Column(Integer, default=0)
    poc_points = Column(Integer, default=0)
    referral_points = Column(Integer, default=0)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    node = relationship('Node', back_populates='rewards')
    
    def to_dict(self):
        """Convert Reward to dictionary."""
        return {
            'id': self.id,
            'node_id': self.node_id,
            'poa_points': self.poa_points,
            'poc_points': self.poc_points,
            'referral_points': self.referral_points,
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

def get_reward_by_id(reward_id):
    """Get a Reward by ID."""
    session = get_session()
    try:
        return session.query(Reward).filter(Reward.id == reward_id).first()
    except Exception as e:
        logger.error(f"Error getting Reward by ID: {str(e)}")
        return None
    finally:
        session.close()

def get_rewards_by_node(node_id):
    """Get all Rewards for a Node."""
    session = get_session()
    try:
        return session.query(Reward).filter(Reward.node_id == node_id).all()
    except Exception as e:
        logger.error(f"Error getting Rewards by Node: {str(e)}")
        return []
    finally:
        session.close()

def get_rewards_by_date_range(node_id, start_date, end_date):
    """Get Rewards for a Node within a date range."""
    session = get_session()
    try:
        return session.query(Reward).filter(
            Reward.node_id == node_id,
            Reward.date >= start_date,
            Reward.date <= end_date
        ).all()
    except Exception as e:
        logger.error(f"Error getting Rewards by date range: {str(e)}")
        return []
    finally:
        session.close()

def create_reward(node_id, date, poa_points=0, poc_points=0, referral_points=0):
    """Create a new Reward."""
    session = get_session()
    try:
        # Check if a reward already exists for this node and date
        existing_reward = session.query(Reward).filter(
            Reward.node_id == node_id,
            Reward.date == date
        ).first()
        
        if existing_reward:
            # Update existing reward
            existing_reward.poa_points += poa_points
            existing_reward.poc_points += poc_points
            existing_reward.referral_points += referral_points
            session.commit()
            return existing_reward
        
        # Create new reward
        reward = Reward(
            node_id=node_id,
            date=date,
            poa_points=poa_points,
            poc_points=poc_points,
            referral_points=referral_points
        )
        session.add(reward)
        session.commit()
        return reward
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating Reward: {str(e)}")
        return None
    finally:
        session.close()

def update_reward(reward_id, **kwargs):
    """Update a Reward."""
    session = get_session()
    try:
        reward = session.query(Reward).filter(Reward.id == reward_id).first()
        if not reward:
            return None
        
        for key, value in kwargs.items():
            if hasattr(reward, key):
                setattr(reward, key, value)
        
        session.commit()
        return reward
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating Reward: {str(e)}")
        return None
    finally:
        session.close()

def delete_reward(reward_id):
    """Delete a Reward."""
    session = get_session()
    try:
        reward = session.query(Reward).filter(Reward.id == reward_id).first()
        if not reward:
            return False
        
        session.delete(reward)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting Reward: {str(e)}")
        return False
    finally:
        session.close()
