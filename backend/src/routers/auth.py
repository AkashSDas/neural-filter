from typing import Annotated, cast
from fastapi import APIRouter, BackgroundTasks, Body, HTTPException, status, Request
from pydantic import EmailStr
from src.schemas.auth import SignupIn, UserInDB, LoginIn, LoginOut, LogoutOut, SignupOut
from src.dependencies import db_dependency, current_user
from src.models.user import User
from src.models.auth import TokenBlacklist
from src.utils.auth import create_access_token
from uuid import uuid4 as uuid
from datetime import datetime, timedelta
from src.utils.email import send_magic_link


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/email-signup", status_code=status.HTTP_201_CREATED)
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
    user = UserInDB(id=new_user.id, username=new_user.username, email=new_user.email).model_dump()  # type: ignore
    return SignupOut(user=user, access_token=access_token).model_dump()  # type: ignore


@router.get("/me", status_code=status.HTTP_200_OK)
async def me(user: current_user, db: db_dependency) -> dict:
    current_user = db.query(User).filter(User.email == user["email"]).first()
    return {
        "user": UserInDB(id=current_user.id, username=current_user.username, email=current_user.email).model_dump()  # type: ignore
    }


@router.post("/email-login", status_code=status.HTTP_200_OK)
async def init_magic_link_login(
    body: Annotated[LoginIn, Body()],
    db: db_dependency,
    background_tasks: BackgroundTasks,
) -> dict:
    user = db.query(User).filter(User.email == body.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    token = str(uuid())
    user.magic_link_token = token  # type: ignore
    user.magic_link_token_expiration = datetime.now() + timedelta(minutes=15)  # type: ignore
    db.commit()

    background_tasks.add_task(send_magic_link, cast(EmailStr, user.email), token)
    return {"message": "Magic link sent to your email"}


@router.get(
    "/email-login/{token}", status_code=status.HTTP_200_OK, response_model=LoginOut
)
async def complete_magic_link_login(token: str, db: db_dependency) -> LoginOut:
    threshold_time = datetime.now() + timedelta(minutes=15)
    user = (
        db.query(User)
        .filter(
            User.magic_link_token == token,
            User.magic_link_token_expiration <= threshold_time,
        )
        .first()
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user.magic_link_token = None  # type: ignore
    user.magic_link_token_expiration = None  # type: ignore
    db.commit()

    access_token = create_access_token(data={"sub": cast(str, user.email)})
    user = UserInDB(id=user.id, username=user.username, email=user.email).model_dump()  # type: ignore
    return LoginOut(user=user, access_token=access_token).model_dump()  # type: ignore


@router.get("/logout", status_code=status.HTTP_200_OK, response_model=LogoutOut)
async def logout(request: Request, user: current_user, db: db_dependency) -> LogoutOut:
    access_token = request.headers.get("Authorization")
    if not isinstance(access_token, str):
        raise HTTPException(status_code=400, detail="Invalid token")
    elif len(access_token.split("Bearer ")) != 2:
        raise HTTPException(status_code=400, detail="Invalid token")
    access_token = access_token.split("Bearer ")[1]

    user = db.query(User).filter(User.email == user["email"]).first()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    db.add(TokenBlacklist(user_id=user.id, access_token=access_token))
    db.commit()
    return LogoutOut(message="Logged out successfully")
