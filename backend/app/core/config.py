"""
Application configuration using Pydantic Settings.
Loads environment variables from .env file.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str
    
    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days
    
    # Application
    PROJECT_NAME: str = "Stock Analysis API"
    DEBUG: bool = True
    
    # CORS - Allow all origins for development (including file://)
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # Groq API
    GROQ_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
