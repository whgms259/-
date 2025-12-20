from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AttendanceBase(BaseModel):
    user_id: int
    check_in_time: datetime
    check_out_time: Optional[datetime] = None

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    user_id: int # Add user_id to the response model
    model_config = ConfigDict(from_attributes=True)
