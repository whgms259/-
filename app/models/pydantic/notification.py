from pydantic import BaseModel, ConfigDict
from datetime import datetime


class NotificationBase(BaseModel):
    message: str


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    read: bool


class Notification(NotificationBase):
    id: int
    user_id: int
    created_at: datetime
    read: bool

    model_config = ConfigDict(from_attributes=True)
