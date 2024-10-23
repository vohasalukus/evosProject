from enum import Enum as PyEnum


from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.repository.base import Base


class UserRole(PyEnum):
    ADMIN = 'admin'
    STAFF = 'staff'
    CUSTOMER = 'customer'


class User(Base):

    name: Mapped[str] = mapped_column(String(256), index=True, nullable=True)
    email: Mapped[str] = mapped_column(String(256), index=True, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(256))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))

