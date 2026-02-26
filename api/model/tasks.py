from sqlalchemy import Column, Integer, String, Boolean,relationship
from api.config.config import Base



class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key = True, index= True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, nullable=False)
    owner = relationship("User", back_populates="create_tasks")