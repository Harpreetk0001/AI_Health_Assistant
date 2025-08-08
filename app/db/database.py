from sqlalchemy import create_engine # Import create_engine to connect to the database
from sqlalchemy.ext.declarative import declarative_base # Import base class for our models
from sqlalchemy.orm import sessionmaker
import os
# Get the database URL from environment variable, or use default if not set
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:Secret#123@localhost:5432/health_assistant")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
