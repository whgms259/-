from sqlalchemy.orm import Session
from ..models.pydantic import attendance as pydantic_attendance
from ..repositories.attendance_repository import AttendanceRepository
from app.models.orm.models import Attendance as orm_attendance
from typing import List, Optional

# Instantiate repository once
attendance_repository = AttendanceRepository()

def get_attendance(db: Session, attendance_id: int) -> Optional[orm_attendance.Attendance]:
    return attendance_repository.get_attendance(db=db, attendance_id=attendance_id)

def get_attendances_by_user(db: Session, user_id: int) -> List[orm_attendance.Attendance]:
    return attendance_repository.get_attendances_by_user(db=db, user_id=user_id)

def create_attendance(db: Session, attendance: pydantic_attendance.AttendanceCreate, user_id: int) -> orm_attendance.Attendance:
    return attendance_repository.create_attendance(db=db, attendance=attendance, user_id=user_id)