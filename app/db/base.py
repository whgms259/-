from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models to ensure they are registered with SQLAlchemy's metadata
from app.models.orm import models
