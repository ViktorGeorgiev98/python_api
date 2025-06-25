from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.schemas import *
from app.utils import *
from app import models
from app import oauth2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    # the user credentials will return username and password
    user = (
        db.query(models.User)
        .filter(
            models.User.email == user_credentials.username,
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=403,
            detail="Invalid credentials",
        )

    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=403,
            detail="Invalid credentials",
        )

    access_token = oauth2.create_access_token(
        data={"user_id": user.id},
    )

    return {"access_token": access_token, "token_type": "bearer"}
