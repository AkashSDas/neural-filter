from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from src.models.user import User
from src.utils.settings import get_settings
from src.utils.database import SessionLocal
from sqlalchemy.orm import Session

settings = get_settings()

# ============================
# Database
# ============================


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# ============================
# Auth
# ============================


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class TokenData(BaseModel):
    email: str | None


class AuthUser(BaseModel):
    email: str | None


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency
) -> dict:
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )

    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        email = payload.get("sub")
        if not isinstance(email, str):
            raise cred_exception
        else:
            token_data = TokenData(email=email)
    except JWTError:
        raise cred_exception

    user = db.query(User).filter(User.email == token_data.email).first()
    if not user:
        raise cred_exception

    return AuthUser(email=user.email).model_dump()  # type: ignore


current_user = Annotated[dict, Depends(get_current_user)]
