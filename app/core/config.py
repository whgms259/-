from pydantic import ConfigDict
from pydantic_settings import BaseSettings
import secrets
from cryptography.fernet import Fernet # Added import

class Settings(BaseSettings):
    # NOTE: This is a placeholder. Replace it with your actual PostgreSQL connection string.
    # The format is: "postgresql://username:password@localhost:5432/app"
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/app"

    # Security settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENCRYPTION_KEY: str = Fernet.generate_key().decode() # Generate a Fernet key

    # ELK Stack Logging
    LOGSTASH_HOST: str = "logstash"
    LOGSTASH_PORT: int = 5000

    model_config = ConfigDict(case_sensitive=True, extra="ignore", env_file=".env")

settings = Settings()