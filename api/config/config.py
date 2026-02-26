from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session,declarative_base
import os

def get_database_url():
    return os.getenv("DATABASE_URL")


engine = create_engine(get_database_url())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = scoped_session(SessionLocal)

Base = declarative_base()

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()