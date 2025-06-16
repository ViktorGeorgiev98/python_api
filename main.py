from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


# Pydantic model for request body validation
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None  # Optional field with default value None


my_posts = [
    {"title": "title of post 1", "content": "content of post 1"}
]  # This will hold our posts in memory (not persistent)


# GET requests


@app.get("/")
async def root():  # async is optional, it is used for asynchronous programming
    return {"message": "Welcome to my FASTAPI project!"}


@app.get("/posts")
async def get_posts():
    return {"data": "This is a post"}


# POST requests
@app.post("/posts")
async def create_post(post: Post):  # Using Body to parse the request body
    print(post)  # This will print the payload to the console
    print(post.rating)
    # convert pydantic model to dictionary
    post_dict = post.dict()
    print(post_dict)
    return {"data": post_dict}


# title str, content str
