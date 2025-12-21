from pydantic import BaseModel

class Recommendation(BaseModel):
    subject: str
    reason: str
