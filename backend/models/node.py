"""
Node model for Sentry Nodes.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base, get_session
import logging

logger = logging.getLogger(__name__)

class Node(Base):
    """Node model for Sentry Nodes."""
    __tablename__ = 'nodes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    vm_id = Column(Integer, ForeignKey('vms.id'))
    status = Column(String(20), default='deploying')
    uptime_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vm = relationship('VM', back_populates='nodes')
    rewards = relationship('Reward', back_populates='node', cascade='all, delete-orphan')
    referrals_as_referrer = relationship('Referral', foreign_keys='Referral.referrer_node_id', back_populates='referrer_node', cascade='all, delete-orphan')
    referrals_as_referred = relationship('Referral', foreign_keys='Referral.referred_node_id', back_populates='referred_node', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert Node to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'vm_id': self.vm_id,
            'status': self.status,
            'uptime_percentage': self.uptime_percentage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def get_node_by_id(node_id):
    """Get a Node by ID."""
    session = get_session()
    try:
        return session.query(Node).filter(Node.id == node_id).first()
    except Exception as e:
        logger.error(f"Error getting Node by ID: {str(e)}")
        return None
    finally:
        session.close()

def get_nodes_by_vm(vm_id):
    """Get all Nodes for a VM."""
    session = get_session()
    try:
        return session.query(Node).filter(Node.vm_id == vm_id).all()
    except Exception as e:
        logger.error(f"Error getting Nodes by VM: {str(e)}")
        return []
    finally:
        session.close()

def create_node(name, vm_id, status='deploying', uptime_percentage=0.0):
    """Create a new Node."""
    session = get_session()
    try:
        node = Node(
            name=name,
            vm_id=vm_id,
            status=status,
            uptime_percentage=uptime_percentage
        )
        session.add(node)
        session.commit()
        return node
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating Node: {str(e)}")
        return None
    finally:
        session.close()

def update_node(node_id, **kwargs):
    """Update a Node."""
    session = get_session()
    try:
        node = session.query(Node).filter(Node.id == node_id).first()
        if not node:
            return None
        
        for key, value in kwargs.items():
            if hasattr(node, key):
                setattr(node, key, value)
        
        session.commit()
        return node
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating Node: {str(e)}")
        return None
    finally:
        session.close()

def delete_node(node_id):
    """Delete a Node."""
    session = get_session()
    try:
        node = session.query(Node).filter(Node.id == node_id).first()
        if not node:
            return False
        
        session.delete(node)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting Node: {str(e)}")
        return False
    finally:
        session.close()
