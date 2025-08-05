import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

# Load environment variables from .env file for DB credentials
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost/dbname")

# Create engine with secure options
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,       # seconds: prevents DB exhaustion attacks
    pool_recycle=1800,     # seconds: refresh idle connections every 30 min
    connect_args={
        "options": "-c statement_timeout=5000"  # 5s query timeout: thwarts slow-query DoS
    },
)

# Create a configurable session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
