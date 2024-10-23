from pydantic import BaseModel, EmailStr
from app.user.models import UserRole


class SUserRegister(BaseModel):
    name: str | None = None
    email: EmailStr
    password: str
    role: UserRole


class SUserAuth(BaseModel):
    email: EmailStr
    password: str

