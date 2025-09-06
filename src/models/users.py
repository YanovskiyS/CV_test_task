import typing

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.jwt import RefreshTokensOrm


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))

    refresh_tokens: Mapped[["RefreshTokensOrm"]] = relationship(
        "RefreshTokensOrm", back_populates="user", cascade="all, delete-orphan"
    )
