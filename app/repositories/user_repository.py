from sqlalchemy.orm import Session
from app.models.orm.models import User as ORMUser
from app.models.pydantic import user as pydantic_user
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["pbkdf2_sha256"]) # Reverted to original scheme

class UserRepository:
    def get_user(self, db: Session, user_id: int) -> Optional[ORMUser]:
        return db.query(ORMUser).filter(ORMUser.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[ORMUser]:
        return db.query(ORMUser).filter(ORMUser.email == email).first()

    def get_user_by_username(self, db: Session, username: str) -> Optional[ORMUser]:
        return db.query(ORMUser).filter(ORMUser.username == username).first()

    def create_user(self, db: Session, user: pydantic_user.UserCreate) -> ORMUser:
        hashed_password = pwd_context.hash(user.password) # Use pwd_context locally
        db_user = ORMUser(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user