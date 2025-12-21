from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    # Use a plain string for the base, as response models will use this
    # and the email will be hashed in the database.
    email: str 
    username: str

class UserCreate(UserBase):
    # Enforce EmailStr validation on creation
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
