from sqlalchemy import Column, Integer, String, DateTime
from src.utils.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    magic_link_token = Column(String, nullable=True)
    magic_link_token_expiration = Column(DateTime, nullable=True)
