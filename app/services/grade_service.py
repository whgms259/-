from sqlalchemy.orm import Session
from ..models.pydantic import grade as pydantic_grade
from ..repositories.grade_repository import GradeRepository
from app.models.orm.models import Grade as ORMGrade
from typing import List, Optional
import pandas as pd

# Instantiate repository once
grade_repository = GradeRepository()

def get_grade(db: Session, grade_id: int) -> Optional[ORMGrade]:
    return grade_repository.get_grade(db=db, grade_id=grade_id)

def get_grades_by_user(db: Session, user_id: int) -> List[ORMGrade]:
    return grade_repository.get_grades_by_user(db=db, user_id=user_id)

def create_grade(db: Session, grade: pydantic_grade.GradeCreate, user_id: int) -> ORMGrade:
    return grade_repository.create_grade(db=db, grade=grade, user_id=user_id)

def get_average_grade_by_subject(db: Session, user_id: int) -> dict:
    """
    Calculates the average grade for a user per subject using Pandas.
    """
    grades = grade_repository.get_grades_by_user(db=db, user_id=user_id)
    if not grades:
        return {}

    # Convert ORM objects to a list of dictionaries for Pandas DataFrame
    grades_data = [{"subject": grade.subject, "score": grade.score} for grade in grades]
    df = pd.DataFrame(grades_data)

    # Calculate average score per subject
    average_grades = df.groupby('subject')['score'].mean().to_dict()
    return average_grades
