from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.schemas import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from app import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET KEY TO SIGN JWT TOKENS
SECRET_KEY = "8D9SADSAIFASD8FUSDFG88FGSD8FDSG8FGFJKDGSG8FDG8878327DFISN8SF3234FDSDFSR32"

# algorithm to encode the JWT
ALGORITHM = "HS256"  # HMAC SHA-256

# Expiration time for the JWT token in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = (
        data.copy()
    )  # Create a copy of the data dictionary to avoid modifying the original
    # Set the expiration time for the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # Add the expiration time to the data
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )  # Encode the token
    return encoded_jwt  # Return the encoded JWT token


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
