from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from src.utils.database import Base
from src.models.user import User


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    blacklisted_on = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    access_token = Column(String, index=True, unique=True)

    user = relationship("User", back_populates="blacklisted_tokens")
