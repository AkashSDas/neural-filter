from typing import Annotated
from fastapi import APIRouter, Body, status
from src.schemas.auth import SignupIn, SignupOut, User, LoginIn, LoginOut, LogoutOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=SignupOut)
async def signup(body: Annotated[SignupIn, Body()]) -> SignupOut:

    return SignupOut(
        user=User(id=1, username=body.username, email=body.email),
        access_token="access_token",
    )


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginOut)
async def login(body: Annotated[LoginIn, Body()]) -> LoginOut:
    return LoginOut(
        user=User(id=1, username=body.username, email=body.email),
        access_token="access_token",
    )


@router.post("/logout", status_code=status.HTTP_200_OK, response_model=LogoutOut)
async def logout() -> LogoutOut:
    return LogoutOut(message="Logged out successfully")
