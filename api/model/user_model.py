from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.config.config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique =True, index=True, nullable=False)
    password = Column(String, nullable =True)
    google_id = Column(String, unique=True, index = True, nullable = True)
    is_google_user = Column(Boolean, default = False)
    is_verified = Column(Boolean, default = False)

    create_tasks = relationship("Tasks", back_populates="owner") 


class VerificationToken(Base):
    __tablename__ = "verification_tokens"
    id=Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp = Column(Integer, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User")


class PasswordReset(Base):
    __tablename__ = "password_resets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp = Column(String, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_used = Column(Boolean, default=False)

    # Relationships
    user = relationship("User")
