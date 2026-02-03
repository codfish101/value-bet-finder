from sqlmodel import SQLModel, create_engine, Session
import os

# Default to SQLite for local, use DATABASE_URL for Production (Render provides this)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bets.db")

# Fix for Render's postgres:// vs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
