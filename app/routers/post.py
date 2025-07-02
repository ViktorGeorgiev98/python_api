from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models
from ..schemas import *
from sqlalchemy.orm import Session
from ..database import get_db
from app import oauth2
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


# GET requests


@router.get("/", response_model=list[PostResponse])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
):
    # normal sql query to get all posts
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = (
        db.query(models.Post).limit(limit).offset(skip).all()
    )  # Using SQLAlchemy to get all posts
    results = (
        db.query(models.Post, func.count(models.Vote.post_id))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .all()
    )  # Get all posts from the database
    return posts  # This will return the list of posts


# get latest posts
# @app.get("/posts/latest")
# def get_latest_post():
#     return {"latest_post": my_posts[-1]}
#     latest_post = my_posts[-1]


# get one post by id
@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # We need to convert id to int since path parameters are strings by default
    # cursor.execute("""SELECT * FROM posts WHERE id =%s""", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        # one way
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": f"Post with id {id} not found"}
        # better way
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    return post


# POST (PUT) requests
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponse,
)  # 201 Created
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):  # Debugging line to check current user
    # Using Body to parse the request body
    # print(post)  # This will print the payload to the console
    # print(post.rating)
    # convert pydantic model to dictionary
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()  # Fetch the newly created post
    # # we need to send status code 201 (created) when a new resource is created
    # conn.commit() Commit the transaction to the database, always required
    # print(**post.dict()) # This will print the dictionary representation of the post
    new_post = models.Post(owner_id=current_user.id, **post.dict())  #
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Refresh the instance to get the new ID and other fields
    return new_post


# title str, content str


# UPDATE requests
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_post(
    id: int,
    updated_post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):  # Using Body to parse the request body
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # update_post = cursor.fetchone()
    # conn.commit()  # Commit the transaction to the database
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.update(
        updated_post.dict(),
        synchronize_session=False,
    )
    db.commit()
    return post_query.first()


# DELETE requests
@router.delete("/{id}", status_code=204)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # find the index in the array that has required id
    # my_posts.pop(index) # remove the post from the list
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()  # Get the first post that matches the id
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    # If the post is deleted successfully, we return a 204 No Content response
    return Response(status_code=status.HTTP_204_NO_CONTENT)
