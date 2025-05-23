from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise Cybersecurity Platform"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Key for encrypting/decrypting sensitive device credentials
    # Generate a strong key using: from cryptography.fernet import Fernet; Fernet.generate_key().decode()
    DEVICE_CREDENTIAL_ENCRYPTION_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings() 