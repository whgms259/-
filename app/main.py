from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .models.pydantic import user as user_model
from .services import user_service
from .db.session import SessionLocal

app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/users/", response_model=user_model.User)
def create_user(user: user_model.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    return user_service.create_user(db=db, user=user)
