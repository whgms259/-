from pydantic import BaseModel, ConfigDict


class GradeBase(BaseModel):
    subject: str
    score: int


class GradeCreate(GradeBase):
    user_id: int


class Grade(GradeBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
