from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AttendanceBase(BaseModel):
    check_in_time: datetime
    check_out_time: Optional[datetime] = None

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)
