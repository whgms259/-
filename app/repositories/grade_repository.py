from sqlalchemy.orm import Session
from app.models.orm.models import Grade as ORMGrade
from app.models.pydantic import grade as pydantic_grade
from typing import List, Optional

class GradeRepository:
    def get_grade(self, db: Session, grade_id: int) -> Optional[ORMGrade]:
        return db.query(ORMGrade).filter(ORMGrade.id == grade_id).first()

    def get_grades_by_user(self, db: Session, user_id: int) -> List[ORMGrade]:
        return db.query(ORMGrade).filter(ORMGrade.user_id == user_id).all()

    def create_grade(self, db: Session, grade: pydantic_grade.GradeCreate, user_id: int) -> ORMGrade:
        grade_data = grade.model_dump()
        grade_data["user_id"] = user_id
        db_grade = ORMGrade(**grade_data)
        db.add(db_grade)
        db.commit()
        db.refresh(db_grade)
        return db_grade
