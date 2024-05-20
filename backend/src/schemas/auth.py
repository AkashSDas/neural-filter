from pydantic import BaseModel, Field, EmailStr, model_validator, validator


class SignupIn(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_]+$",
        examples=["akash", "AkashSDas"],
    )

    email: EmailStr = Field(..., examples=["akash@gmail.com"])


class UserInDB(BaseModel):
    id: int
    username: str
    email: EmailStr


class SignupOut(BaseModel):
    user: UserInDB
    access_token: str


class LoginIn(BaseModel):
    email: EmailStr = Field(..., examples=["akash@gmail.com"])


class LoginOut(BaseModel):
    user: UserInDB
    access_token: str


class LogoutOut(BaseModel):
    message: str
