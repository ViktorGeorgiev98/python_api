from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models
from ..schemas import *
from ..utils import *
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


# USERS RELATED ENDPOINTS
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # hash the password before storing it
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    return user


@router.get("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    pass
