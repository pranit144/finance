"""
User database model using SQLAlchemy ORM.
"""
import enum
from sqlalchemy import Column, String, Boolean, Enum, DateTime
from datetime import datetime
import uuid

from ..core.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "ADMIN"
    STAFF = "STAFF"


class User(Base):
    """User model for authentication and authorization."""
    
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STAFF)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<User {self.email}>"
