from sqlalchemy.orm import Session
from app.models.orm import user as orm_user
from app.models.pydantic import user as pydantic_user
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def get_user(self, db: Session, user_id: int):
        return db.query(orm_user.User).filter(orm_user.User.id == user_id).first()

    def create_user(self, db: Session, user: pydantic_user.UserCreate):
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