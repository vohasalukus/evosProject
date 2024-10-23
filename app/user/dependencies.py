from datetime import datetime

from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError, ExpiredSignatureError
from app.config import settings
from app.exceptions import IncorrectTokenException, TokenExpiredException, UserIsNotPresentException
from app.user.models import User

KEY = settings.KEY
ALGORITHM = settings.ALGORITHM


def get_token(request: Request = None):
    token = request.cookies.get("access_token")
    if not token:
        token = request.headers.get("Authorization")
        if not token:
            raise IncorrectTokenException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await User.find_by_id(int(user_id))

    if not user:
        raise UserIsNotPresentException
    await User.update(model_id=user.id, last_login=datetime.utcnow())

    return user
