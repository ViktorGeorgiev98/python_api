from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


# Pydantic model for request body validation


# USER RELATED SCHEMAS
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# TOKEN RELATED SCHEMAS


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# POST RELATED SCHEMAS


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime
    id: int
    owner_id: int
    owner: UserOut  # Assuming UserOut is defined in the schemas


class PostOut(PostBase):
    post: PostResponse
    votes: int  # Number of votes on the post


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # 1 for new vote, 0 for removing a vote
