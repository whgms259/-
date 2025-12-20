from sqlalchemy.orm import Session
from app.models.orm.models import Attendance as orm_attendance
from app.models.pydantic import attendance as pydantic_attendance
from typing import List, Optional

class AttendanceRepository:
    def get_attendance(self, db: Session, attendance_id: int) -> Optional[orm_attendance.Attendance]:
        return db.query(orm_attendance).filter(orm_attendance.id == attendance_id).first()

    def get_attendances_by_user(self, db: Session, user_id: int) -> List[orm_attendance.Attendance]:
        return db.query(orm_attendance).filter(orm_attendance.user_id == user_id).all()

    def create_attendance(self, db: Session, attendance: pydantic_attendance.AttendanceCreate) -> orm_attendance.Attendance:
        db_attendance = orm_attendance(**attendance.model_dump())
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance