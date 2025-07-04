from fastapi import FastAPI
from app import models
from app.database import engine
from .routers import post, user, auth, vote
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware


# specify the origins that are allowed to access the API
origins = ["*"]  # Allow all origins, you can specify a list of allowed origins instead

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# models.Base.metadata.create_all(bind=engine)  # Create all tables in the database
print("✅ Tables creation triggered")


# GET requests
@app.get("/")
async def root():  # async is optional, it is used for asynchronous programming
    return {"message": "Welcome to my FASTAPI project!"}


app.include_router(post.router)  # Include the post router
app.include_router(user.router)  # Include the user router
app.include_router(auth.router)  # Include the auth router
app.include_router(vote.router)  # Include the vote router
