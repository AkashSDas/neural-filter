from src.utils.settings import get_settings
from datetime import timedelta, datetime
from copy import deepcopy
from jose import JWTError, jwt


settings = get_settings()


def create_access_token(data: dict) -> str:
    to_encode = deepcopy(data)
    expire = datetime.now() + timedelta(minutes=settings.jwt_expiry_in_min)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def verify_access_token(token: str) -> None | str:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        email = payload.get("sub")
        if email is None:
            raise JWTError()
        return email
    except JWTError:
        return None
