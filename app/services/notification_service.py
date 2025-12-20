from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.notification_repository import NotificationRepository
from app.models.orm.models import Notification as orm_notification
from app.models.pydantic.notification import NotificationCreate, NotificationUpdate


class NotificationService:
    def __init__(self):
        self.repo = NotificationRepository()

    def create_notification(self, db: Session, *, notification: NotificationCreate) -> orm_notification.Notification:
        return self.repo.create(db=db, obj_in=notification)

    def get_notifications_by_user(self, db: Session, *, user_id: int) -> List[orm_notification.Notification]:
        return self.repo.get_by_user_id(db=db, user_id=user_id)

    def mark_as_read(self, db: Session, *, notification_id: int) -> Optional[orm_notification.Notification]:
        notification = self.repo.get(db=db, id=notification_id)
        if not notification:
            return None
        
        update_data = NotificationUpdate(read=True)
        return self.repo.update(db=db, db_obj=notification, obj_in=update_data)