from sqlalchemy.orm import Session
from app.models.orm import user as orm_user
from app.models.pydantic import user as pydantic_user
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["pbkdf2_sha256"])

class UserRepository:
    def get_user(self, db: Session, user_id: int) -> Optional[orm_user.User]:
        return db.query(orm_user.User).filter(orm_user.User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[orm_user.User]:
        return db.query(orm_user.User).filter(orm_user.User.email == email).first()

    def get_user_by_username(self, db: Session, username: str) -> Optional[orm_user.User]:
        return db.query(orm_user.User).filter(orm_user.User.username == username).first()

    def create_user(self, db: Session, user: pydantic_user.UserCreate) -> orm_user.User:
        hashed_password = pwd_context.hash(user.password)
        db_user = orm_user.User(
            email=user.email, 
            username=user.username, 
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user