from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import models
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.schemas import *
from app.utils import *

app = FastAPI()
models.Base.metadata.create_all(bind=engine)  # Create all tables in the database
print("✅ Tables creation triggered")

# Dependency to get a database session
get_db()


# only for manual work with the database !!!!
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="Viktor1902",
#             cursor_factory=RealDictCursor,  # This will return results as dictionaries
#         )
#         cursor = conn.cursor()
#         print("Database connection established successfully.")
#         break
#     except Exception as e:
#         print("Connection to the database failed.")
#         print(e)
#         time.sleep(2)


# Pydantic model for request body validation


# GET requests


@app.get("/")
async def root():  # async is optional, it is used for asynchronous programming
    return {"message": "Welcome to my FASTAPI project!"}


@app.get("/posts", response_model=list[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    # normal sql query to get all posts
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()  # Using SQLAlchemy to get all posts
    return posts  # This will return the list of posts


# get latest posts
# @app.get("/posts/latest")
# def get_latest_post():
#     return {"latest_post": my_posts[-1]}
#     latest_post = my_posts[-1]


# get one post by id
@app.get("/posts/{id}", response_model=PostResponse)
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
@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)  # 201 Created
async def create_post(
    post: PostCreate, db: Session = Depends(get_db)
):  # Using Body to parse the request body
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
    new_post = models.Post(**post.dict())  #
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Refresh the instance to get the new ID and other fields
    return new_post


# title str, content str


# UPDATE requests
@app.put(
    "/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse
)
def update_post(
    id: int, updated_post: PostCreate, db: Session = Depends(get_db)
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

    post_query.update(
        updated_post.dict(),
        synchronize_session=False,
    )
    db.commit()
    return post_query.first()


# DELETE requests
@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):
    # find the index in the array that has required id
    # my_posts.pop(index) # remove the post from the list
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    post.delete(synchronize_session=False)
    db.commit()
    # If the post is deleted successfully, we return a 204 No Content response
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# USERS RELATED ENDPOINTS
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # hash the password before storing it
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    return user
