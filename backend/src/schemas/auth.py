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

    @model_validator(mode="after")  # type: ignore
    @classmethod
    def check_if_credentials_are_unique(cls, instance: "SignupIn") -> "SignupIn":
        if False:
            raise ValueError("Username or email already exists")
        return instance


class User(BaseModel):
    id: int
    username: str
    email: EmailStr


class SignupOut(BaseModel):
    user: User
    access_token: str


class LoginIn(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_]+$",
        examples=["akash", "AkashSDas"],
    )

    email: EmailStr = Field(..., examples=["akash@gmail.com"])


class LoginOut(BaseModel):
    user: User
    access_token: str


class LogoutOut(BaseModel):
    message: str
