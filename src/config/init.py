from pydantic import BaseSettings, MySQLDsn
from typing import List, Optional

class Settings(BaseSettings):
    # MySQL Specific Settings
    DATABASE_HOST: str = 'localhost'
    DATABASE_PORT: int = 3306
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str = 'imageprocessing'
    
    # Database URL for SQLAlchemy
    DATABASE_URL: MySQLDsn

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings()