from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


# Pydantic model for request body validation
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None  # Optional field with default value None


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
    {"title": "title of post 3", "content": "content of post 3", "id": 3},
]  # This will hold our posts in memory (not persistent)


# GET requests


@app.get("/")
async def root():  # async is optional, it is used for asynchronous programming
    return {"message": "Welcome to my FASTAPI project!"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}  # This will return the list of posts


# get latest posts
@app.get("/posts/latest")
def get_latest_post():
    return {"latest_post": my_posts[-1]}
    latest_post = my_posts[-1]


# get one post by id
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # We need to convert id to int since path parameters are strings by default
    post = find_post(id)
    if not post:
        # one way
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": f"Post with id {id} not found"}
        # better way
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    return {"post_detail": f"Here is post {post}"}


# POST (PUT) requests
@app.post("/posts", status_code=status.HTTP_201_CREATED)  # 201 Created
async def create_post(post: Post):  # Using Body to parse the request body
    print(post)  # This will print the payload to the console
    print(post.rating)
    # convert pydantic model to dictionary
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    # we need to send status code 201 (created) when a new resource is created
    return {"data": post_dict}


# title str, content str


# UPDATE requests
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    if not find_post(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    index = find_index_post(id)
    my_posts[index] = post.dict()
    my_posts[index]["id"] = id  # keep the same id
    return {"updated_post": my_posts[index]}


# DELETE requests
@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    # find the index in the array that has required id
    # my_posts.pop(index) # remove the post from the list
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    my_posts.pop(index)
    # If the post is deleted successfully, we return a 204 No Content response
    return Response(status_code=status.HTTP_204_NO_CONTENT)
