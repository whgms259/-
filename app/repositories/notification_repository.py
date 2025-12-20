from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.orm.models import Notification
from app.models.pydantic.notification import NotificationCreate, NotificationUpdate


class NotificationRepository:
    def create(self, db: Session, *, obj_in: NotificationCreate) -> Notification:
        db_obj = Notification(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user_id(self, db: Session, *, user_id: int) -> List[Notification]:
        return db.query(Notification).filter(Notification.user_id == user_id).all()

    def get(self, db: Session, *, id: int) -> Optional[Notification]:
        return db.query(Notification).filter(Notification.id == id).first()

    def update(self, db: Session, *, db_obj: Notification, obj_in: NotificationUpdate) -> Notification:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj