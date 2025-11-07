from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@postgres:5432/littlemonster"
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    service_port: int = 8013
    
    class Config:
        env_file = ".env"

settings = Settings()
