import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
# To load environment variables from .env file for DB credentials
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:Secret#123@localhost:5432/health_assistant")
# To create engine with secure options
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,       # it's in seconds and will prevent DB exhaustion attacks
    pool_recycle=1800,     # it's in seconds and will refresh idle connections every 30 min
    connect_args={
        "options": "-c statement_timeout=5000"  # 5s query timeout: thwarts slow-query DoS
    },
)
# To create a configurable session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
#  FastAPI dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
