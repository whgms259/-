from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.notification_repository import NotificationRepository
from app.models.orm.models import Notification as orm_notification
from app.models.pydantic.notification import NotificationCreate, NotificationUpdate
from app.core.websockets import manager
import json

class NotificationService:
    def __init__(self):
        self.repo = NotificationRepository()

    async def create_notification(self, db: Session, *, notification: NotificationCreate, user_id: int) -> orm_notification:
        notification_data = notification.model_dump()
        notification_data["user_id"] = user_id
        created_notification = self.repo.create(db=db, obj_in=notification_data)
        
        # Broadcast the new notification to the user
        message = {
            "type": "new_notification",
            "data": {
                "id": created_notification.id,
                "message": created_notification.message,
                "read": created_notification.read,
                "created_at": created_notification.created_at.isoformat()
            }
        }
        await manager.broadcast_to_user(json.dumps(message), user_id)
        
        return created_notification

    def get_notifications_by_user(self, db: Session, *, user_id: int) -> List[orm_notification]:
        return self.repo.get_by_user_id(db=db, user_id=user_id)

    def mark_as_read(self, db: Session, *, notification_id: int) -> Optional[orm_notification]:
        notification = self.repo.get(db=db, id=notification_id)
        if not notification:
            return None
        
        update_data = NotificationUpdate(read=True)
        return self.repo.update(db=db, db_obj=notification, obj_in=update_data)