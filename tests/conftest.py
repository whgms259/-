import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.db.base import Base
from app.core.config import settings # Import settings

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    # Set a consistent SECRET_KEY for testing
    settings.SECRET_KEY = "test-secret-key-for-testing"
    
    # Before tests run, create the tables
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # After tests run, drop the tables
    Base.metadata.drop_all(bind=engine)
