from typing import Annotated
from fastapi import Depends
from src.utils.database import SessionLocal
from sqlalchemy.orm import Session


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
