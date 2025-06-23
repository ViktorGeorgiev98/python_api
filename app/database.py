from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# How to use SQLAlchemy with FastAPI to use normal python code to work with the database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Viktor1902@localhost/fastapi"


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
