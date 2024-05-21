from sqlalchemy import Column, Integer, String, DateTime
from src.utils.database import Base
from sqlalchemy.orm import relationship
from src.models.follow import Follow


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    magic_link_token = Column(String, nullable=True)
    magic_link_token_expiration = Column(DateTime, nullable=True)

    blacklisted_tokens = relationship("TokenBlacklist", back_populates="user")
    following = relationship(
        "Follow", foreign_keys=[Follow.follower_id], back_populates="follower"
    )
    followers = relationship(
        "Follow", foreign_keys=[Follow.followed_id], back_populates="followed"
    )
