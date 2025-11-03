"""
Configuration for Study Analytics Service
"""
import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Service configuration"""
    
    # Service
    service_name: str = "study-analytics"
    service_port: int = 8012
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/littlemonster"
    
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003"
    
    # External Services
    gamification_service_url: str = "http://localhost:8011"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into list"""
        return [origin.strip() for origin in self.cors_origins.split(',')]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
