"""
Configuration settings for the FastAPI application
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    # API Settings
    app_name: str = "Student Enrollment API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    
    # Database Settings
    database_url: str = "sqlite:///./student_enrollment.db"
    
    # CORS Settings
    cors_origins: list[str] = ["http://localhost:5000", "http://localhost:5001", "http://127.0.0.1:5000", "http://127.0.0.1:5001"]
    
    # Pagination Settings
    default_page_size: int = 20
    max_page_size: int = 100
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create settings instance
settings = Settings()