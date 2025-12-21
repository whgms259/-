import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.services import user_service

# Use pbkdf2_sha256 to avoid bcrypt issues during initial setup
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(BaseModel):
    user_id: Optional[int] = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_field_hash(field: str) -> str:
    """
    Creates a deterministic SHA256 hash of a field using the app's secret key.
    """
    secret_key_bytes = settings.SECRET_KEY.encode()
    combined_input = f"{field}".encode() + secret_key_bytes
    hashed_value = hashlib.sha256(combined_input).hexdigest()
    return hashed_value

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

from app.models.orm.models import User as ORMUser

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
        token_data = TokenData(user_id=user_id)
    except (JWTError, ValueError):
        raise credentials_exception
    
    user = user_service.get_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_ws(token: str, db: Session) -> Optional[ORMUser]:
    """
    Dependency for WebSocket authentication.
    Reads token from query param and returns user, or None if invalid.
    """
    if not token:
        return None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            return None
        user_id = int(user_id_str)
        token_data = TokenData(user_id=user_id)
    except (JWTError, ValueError):
        return None
    
    user = user_service.get_user(db, user_id=token_data.user_id)
    return user
