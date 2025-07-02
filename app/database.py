from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
from app.config import settings


# How to use SQLAlchemy with FastAPI to use normal python code to work with the database
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session to the caller
    finally:
        db.close()


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
