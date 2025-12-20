from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # NOTE: This is a placeholder. Replace it with your actual PostgreSQL connection string.
    # The format is: "postgresql://username:password@localhost:5432/app"
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/app"

    model_config = ConfigDict(case_sensitive=True, extra="ignore", env_file=".env")

settings = Settings()