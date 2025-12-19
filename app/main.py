from fastapi import FastAPI
from .models import user as user_model
from .services import user_service

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/users/", response_model=user_model.User)
def create_user(user: user_model.UserCreate):
    """
    Create a new user.
    """
    return user_service.create_user(user=user)
