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
from .routers import post, user, auth

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


# GET requests
@app.get("/")
async def root():  # async is optional, it is used for asynchronous programming
    return {"message": "Welcome to my FASTAPI project!"}


app.include_router(post.router)  # Include the post router
app.include_router(user.router)  # Include the user router
app.include_router(auth.router)  # Include the auth router
