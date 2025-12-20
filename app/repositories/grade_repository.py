from sqlalchemy.orm import Session
from typing import List
from app.models.orm.models import Grade
from app.models.pydantic.grade import GradeCreate


class GradeRepository:
    def create(self, db: Session, *, obj_in: GradeCreate) -> Grade:
        db_obj = Grade(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user_id(self, db: Session, *, user_id: int) -> List[Grade]:
        return db.query(Grade).filter(Grade.user_id == user_id).all()