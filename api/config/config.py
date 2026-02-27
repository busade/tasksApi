from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session,declarative_base
from dotenv import load_dotenv
load_dotenv()
import os

def get_database_url():
    return os.getenv("DATABASE_URL","sqlite:///./test.db")


engine = create_engine(
    get_database_url(),
    pool_size=10,            # number of persistent connections
    max_overflow=20,         # extra temporary connections
    pool_pre_ping=True 
                       )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = scoped_session(SessionLocal)

Base = declarative_base()

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()