from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from api.config.config import Base



class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key = True, index= True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer,ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="create_tasks", foreign_keys=[owner_id])