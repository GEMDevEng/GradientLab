"""
VM model for cloud virtual machines.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base, get_session
import logging

logger = logging.getLogger(__name__)

class VM(Base):
    """VM model for cloud virtual machines."""
    __tablename__ = 'vms'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    provider = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)
    instance_type = Column(String(50))
    vm_id = Column(String(255), unique=True)
    ip_address = Column(String(50))
    status = Column(String(20), default='provisioning')
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='vms')
    nodes = relationship('Node', back_populates='vm', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert VM to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'region': self.region,
            'instance_type': self.instance_type,
            'vm_id': self.vm_id,
            'ip_address': self.ip_address,
            'status': self.status,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def get_vm_by_id(vm_id):
    """Get a VM by ID."""
    session = get_session()
    try:
        return session.query(VM).filter(VM.id == vm_id).first()
    except Exception as e:
        logger.error(f"Error getting VM by ID: {str(e)}")
        return None
    finally:
        session.close()

def get_vm_by_provider_id(provider_id):
    """Get a VM by provider ID."""
    session = get_session()
    try:
        return session.query(VM).filter(VM.vm_id == provider_id).first()
    except Exception as e:
        logger.error(f"Error getting VM by provider ID: {str(e)}")
        return None
    finally:
        session.close()

def get_vms_by_user(user_id):
    """Get all VMs for a user."""
    session = get_session()
    try:
        return session.query(VM).filter(VM.user_id == user_id).all()
    except Exception as e:
        logger.error(f"Error getting VMs by user: {str(e)}")
        return []
    finally:
        session.close()

def create_vm(name, provider, region, instance_type, user_id, vm_id=None, ip_address=None, status='provisioning'):
    """Create a new VM."""
    session = get_session()
    try:
        vm = VM(
            name=name,
            provider=provider,
            region=region,
            instance_type=instance_type,
            vm_id=vm_id,
            ip_address=ip_address,
            status=status,
            user_id=user_id
        )
        session.add(vm)
        session.commit()
        return vm
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating VM: {str(e)}")
        return None
    finally:
        session.close()

def update_vm(vm_id, **kwargs):
    """Update a VM."""
    session = get_session()
    try:
        vm = session.query(VM).filter(VM.id == vm_id).first()
        if not vm:
            return None
        
        for key, value in kwargs.items():
            if hasattr(vm, key):
                setattr(vm, key, value)
        
        session.commit()
        return vm
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating VM: {str(e)}")
        return None
    finally:
        session.close()

def delete_vm(vm_id):
    """Delete a VM."""
    session = get_session()
    try:
        vm = session.query(VM).filter(VM.id == vm_id).first()
        if not vm:
            return False
        
        session.delete(vm)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting VM: {str(e)}")
        return False
    finally:
        session.close()
