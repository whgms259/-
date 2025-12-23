from fastapi import FastAPI, Depends, HTTPException, status, Response, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from prometheus_client import generate_latest
import logging
import logstash

from .models.pydantic import user as pydantic_user_model
from .models.pydantic import attendance as pydantic_attendance_model
from .models.pydantic import grade as pydantic_grade_model
from .models.pydantic import notification as pydantic_notification_model
from .models.pydantic import token as pydantic_token_model
from .models.pydantic import recommendation as pydantic_recommendation_model
from .services import user_service, attendance_service, grade_service, notification_service, recommendation_service
from .core import security
from .db.session import get_db
from .core.config import settings
from .core.websockets import manager
from .models.orm.models import User as ORMUser

# Configure logging
host = settings.LOGSTASH_HOST
port = settings.LOGSTASH_PORT

# Create a logger
logger = logging.getLogger('fastapi-app')
logger.setLevel(logging.INFO)

# Add the Logstash handler
logger.addHandler(logstash.TCPLogstashHandler(host, port, version=1))

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/frontend", response_class=HTMLResponse, include_in_schema=False)
async def read_frontend():
    with open("app/static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"Hello": "World"}

@app.get("/metrics")
def get_metrics():
    return Response(content=generate_latest().decode("utf-8"), media_type="text/plain")

@app.post("/token", response_model=pydantic_token_model.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_service.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=pydantic_user_model.User)
def create_user_api(user: pydantic_user_model.UserCreate, db: Session = Depends(get_db)):
    existing_user_email = user_service.get_user_by_email(db, email=user.email)
    existing_user_username = user_service.get_user_by_username(db, username=user.username)
    if existing_user_email or existing_user_username:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    return user_service.create_user(db=db, user=user)

@app.get("/users/me/recommendations", response_model=List[pydantic_recommendation_model.Recommendation])
def get_my_recommendations_api(db: Session = Depends(get_db), current_user: ORMUser = Depends(security.get_current_user)):
    return recommendation_service.get_recommendations_for_user(db=db, user_id=current_user.id)

@app.post("/attendances/", response_model=pydantic_attendance_model.Attendance)
def create_attendance_api(attendance: pydantic_attendance_model.AttendanceCreate, db: Session = Depends(get_db), current_user: ORMUser = Depends(security.get_current_user)):
    return attendance_service.create_attendance(db=db, attendance=attendance, user_id=current_user.id)

@app.get("/attendances/me", response_model=List[pydantic_attendance_model.Attendance])
def get_my_attendances_api(db: Session = Depends(get_db), current_user: ORMUser = Depends(security.get_current_user)):
    return attendance_service.get_attendances_by_user(db=db, user_id=current_user.id)

@app.post("/grades/", response_model=pydantic_grade_model.Grade)
def create_grade_api(grade: pydantic_grade_model.GradeCreate, db: Session = Depends(get_db), current_user: ORMUser = Depends(security.get_current_user)):
    return grade_service.create_grade(db=db, grade=grade, user_id=current_user.id)

@app.get("/grades/me", response_model=List[pydantic_grade_model.Grade])
def get_my_grades_api(db: Session = Depends(get_db), current_user: ORMUser = Depends(security.get_current_user)):
    return grade_service.get_grades_by_user(db=db, user_id=current_user.id)

@app.get("/grades/me/average", response_model=dict)
def get_my_average_grades_api(db: Session = Depends(get_db), current_user: ORMUser = Depends(security.get_current_user)):
    average_grades = grade_service.get_average_grade_by_subject(db=db, user_id=current_user.id)
    if not average_grades:
        raise HTTPException(status_code=404, detail="No grades found for the user.")
    return average_grades

@app.get("/notifications/me", response_model=List[pydantic_notification_model.Notification])
def get_my_notifications_api(db: Session = Depends(get_db), current_user: ORMUser = Depends(security.get_current_user)):
    service = notification_service.NotificationService()
    return service.get_notifications_by_user(db=db, user_id=current_user.id)

@app.post("/notifications/", response_model=pydantic_notification_model.Notification)
async def create_notification_api(notification: pydantic_notification_model.NotificationCreate, db: Session = Depends(get_db), current_user: ORMUser = Depends(security.get_current_user)):
    service = notification_service.NotificationService()
    return await service.create_notification(db=db, notification=notification, user_id=current_user.id)

@app.patch("/notifications/{notification_id}/read", response_model=pydantic_notification_model.Notification)
def mark_notification_as_read_api(notification_id: int, db: Session = Depends(get_db), current_user: ORMUser = Depends(security.get_current_user)):
    service = notification_service.NotificationService()
    notification = service.mark_as_read(db=db, notification_id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to mark this notification as read")
    return notification

@app.websocket("/ws/notifications")
async def websocket_notification_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    user = await security.get_current_user_ws(token=token, db=db)
    if user is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, user.id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)
