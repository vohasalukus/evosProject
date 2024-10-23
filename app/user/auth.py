from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings
from app.user.models import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
KEY = settings.KEY
ALGORITHM = settings.ALGORITHM
TOKEN_EXPIRE = settings.TOKEN_EXPIRE


def get_hashed_password(password: str):
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_context.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.KEY, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: str, password: str):
    user = await User.find_one_or_none(User.email == email)

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user
