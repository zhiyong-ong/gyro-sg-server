from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import CONFIG

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any]
) -> str:
    to_encode = {"sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, CONFIG.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
