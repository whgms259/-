from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .models.pydantic import user as pydantic_user_model
from .models.pydantic import attendance as pydantic_attendance_model
from .models.pydantic import grade as pydantic_grade_model
from .models.pydantic import notification as pydantic_notification_model
from .services import user_service, attendance_service, grade_service, notification_service
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

@app.post("/grades/", response_model=pydantic_grade_model.Grade)
def create_grade_api(grade: pydantic_grade_model.GradeCreate, db: Session = Depends(get_db)):
    """
    Create a new grade record.
    """
    # Check if user exists
    user = user_service.get_user(db, user_id=grade.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    service = grade_service.GradeService()
    return service.create_grade(db=db, grade=grade)

@app.get("/users/{user_id}/grades/", response_model=List[pydantic_grade_model.Grade])
def get_user_grades_api(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all grade records for a specific user.
    """
    # Check if user exists
    user = user_service.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    service = grade_service.GradeService()
    return service.get_grades_by_user(db=db, user_id=user_id)

@app.get("/users/{user_id}/notifications/", response_model=List[pydantic_notification_model.Notification])
def get_user_notifications_api(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all notifications for a specific user.
    """
    user = user_service.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    service = notification_service.NotificationService()
    return service.get_notifications_by_user(db=db, user_id=user_id)

@app.post("/notifications/", response_model=pydantic_notification_model.Notification)
def create_notification_api(notification: pydantic_notification_model.NotificationCreate, db: Session = Depends(get_db)):
    """
    Create a new notification.
    """
    user = user_service.get_user(db, user_id=notification.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    service = notification_service.NotificationService()
    return service.create_notification(db=db, notification=notification)

@app.patch("/notifications/{notification_id}/read", response_model=pydantic_notification_model.Notification)
def mark_notification_as_read_api(notification_id: int, db: Session = Depends(get_db)):
    """
    Mark a notification as read.
    """
    service = notification_service.NotificationService()
    notification = service.mark_as_read(db=db, notification_id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification