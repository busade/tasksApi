from sqlalchemy import Column, Integer, String, Boolean,relationship, DateTime
from api.config.config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique =True, index=True, nullable=False)
    password = Column(String, nullable =True)
    google_id = Column(String, unique=True, index = True, nullable = True)
    is_google_user = Column(Boolean, default = False)
    is_verified = Column(Boolean, default = False)
    verification_token_id = Column(String, ForeignKey("verification_tokens.id", ondelete="SET NULL"), nullable=True)

    verification_token = relationship("VerificationToken", back_populates="user")
    create_tasks = relationship("Task", back_populates="owner") 


class VerificationToken(BaseTableModel):
    __tablename__ = "verification_tokens"

    value = Column(Integer, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    user = relationship("User", back_populates="verification_token", uselist=False)
