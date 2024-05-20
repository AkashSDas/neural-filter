from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, status
from src.schemas.auth import SignupIn, UserInDB, LoginIn, LoginOut, LogoutOut
from src.dependencies import db_dependency
from src.models.user import User
from src.utils.auth import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(body: Annotated[SignupIn, Body()], db: db_dependency) -> dict:
    db_user = (
        db.query(User)
        .filter((User.email == body.email) | (User.username == body.username))
        .first()
    )
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already taken")

    new_user = User(username=body.username, email=body.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.email})
    return {"user": new_user, "access_token": access_token}


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginOut)
async def login(body: Annotated[LoginIn, Body()]) -> LoginOut:
    return LoginOut(
        user=UserInDB(id=1, username=body.username, email=body.email),
        access_token="access_token",
    )


@router.post("/logout", status_code=status.HTTP_200_OK, response_model=LogoutOut)
async def logout() -> LogoutOut:
    return LogoutOut(message="Logged out successfully")
