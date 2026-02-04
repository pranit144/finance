"""
Pydantic schemas for authentication requests and responses.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserSignup(BaseModel):
    """Schema for user signup request."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8, max_length=100)
    role: str = Field(default="STAFF", pattern="^(ADMIN|STAFF)$")


class UserLogin(BaseModel):
    """Schema for user login request."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user data response."""
    id: UUID
    email: str
    name: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows creation from ORM models


class MessageResponse(BaseModel):
    """Generic message response schema."""
    message: str
