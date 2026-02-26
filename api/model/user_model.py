from sqlalchemy import Column, Integer, String, Boolean,relationship
from api.config.config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique =True, index=True, nullable=False)
    password = Column(String, nullable =True)
    google_id = Column(String, unique=True, index = True, nullable = True)
    is_google_user = Column(Boolean, default = False)
    create_tasks = relationship("Task", back_populates="owner") 