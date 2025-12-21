from pydantic import BaseModel, ConfigDict
from typing import Optional

class GradeBase(BaseModel):
    subject: str
    score: int

class GradeCreate(GradeBase):
    pass

class Grade(GradeBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)