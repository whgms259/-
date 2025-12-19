from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .models.pydantic import user as pydantic_user_model
from .models.pydantic import attendance as pydantic_attendance_model
from .services import user_service, attendance_service
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

@app.post("/users/", response_model=pydantic_user_model.User)
def create_user_api(user: pydantic_user_model.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    # Check if a user with the same email or username already exists
    existing_user_email = user_service.get_user_by_email(db, email=user.email)
    existing_user_username = user_service.get_user_by_username(db, username=user.username)
    if existing_user_email or existing_user_username:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    return user_service.create_user(db=db, user=user)

@app.post("/attendances/", response_model=pydantic_attendance_model.Attendance)
def create_attendance_api(attendance: pydantic_attendance_model.AttendanceCreate, db: Session = Depends(get_db)):
    """
    Create a new attendance record (check-in/check-out).
    """
    # Check if user exists
    user = user_service.get_user(db, user_id=attendance.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return attendance_service.create_attendance(db=db, attendance=attendance)

@app.get("/users/{user_id}/attendances/", response_model=List[pydantic_attendance_model.Attendance])
def get_user_attendances_api(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all attendance records for a specific user.
    """
    # Check if user exists
    user = user_service.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return attendance_service.get_attendances_by_user(db=db, user_id=user_id)
