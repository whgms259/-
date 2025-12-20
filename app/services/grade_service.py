from sqlalchemy.orm import Session
from app.repositories.grade_repository import GradeRepository
from app.models.pydantic.grade import GradeCreate
from app.models.orm.models import Grade as orm_grade
from typing import List

class GradeService:
    def __init__(self):
        self.repo = GradeRepository()

    def create_grade(self, db: Session, *, grade: GradeCreate) -> orm_grade.Grade:
        return self.repo.create(db=db, obj_in=grade)

    def get_grades_by_user(self, db: Session, *, user_id: int) -> List[orm_grade.Grade]:
        return self.repo.get_by_user_id(db=db, user_id=user_id)