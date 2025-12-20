from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    attendances = relationship("Attendance", back_populates="owner")
    grades = relationship("Grade", back_populates="user")

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    check_in_time = Column(DateTime(timezone=True))
    check_out_time = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id")) # Renamed owner_id to user_id

    owner = relationship("User", back_populates="attendances")

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    score = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="grades")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
