from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # NOTE: This is a placeholder. Replace it with your actual PostgreSQL connection string.
    # The format is: "postgresql://username:password@host:port/database_name"
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/app"

    class Config:
        case_sensitive = True

settings = Settings()
