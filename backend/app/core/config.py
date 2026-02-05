"""
Application configuration using Pydantic Settings.
Loads environment variables from .env file.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database: Use local sqlite file in the app directory
    DATABASE_URL: str = "sqlite:///./stock_analysis_prod.db"
    
    # JWT Settings
    SECRET_KEY: str = "development_secret_key_change_in_production"
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
