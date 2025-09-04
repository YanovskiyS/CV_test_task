import uuid
from datetime import datetime, timezone, timedelta
from typing import Tuple, Optional

import jwt
from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, PyJWTError
from passlib.context import CryptContext

from src.config import settings
from src.database import async_session_maker
from src.repositiries.jwt import JwtRepository


class TokenError(Exception):
    pass

class AuthService:
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    async def verify_refresh_token(refresh_token: str, conn) -> tuple[int, str]:
        try:
            payload = jwt.decode(
                refresh_token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
        except PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        # проверка что это именно refresh-токен
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a refresh token")

        jti = payload.get("jti")
        user_id = int(payload.get("sub"))

        # проверяем в базе
        repo = JwtRepository(conn)
        db_token = await repo.get_token_by_id(jti)

        if not db_token or db_token.revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked or not found")

        if db_token.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired in DB")

        return user_id, jti

    def hash_password(self, password: str) -> str:
        return self.pwd_ctx.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        return self.pwd_ctx.verify(password, password_hash)

    def _encode(self, payload: dict, expires_delta: timedelta) -> str:
        now = datetime.now(timezone.utc)
        exp = now + expires_delta
        to_encode = {**payload, "exp": exp, "iat": now, "nbf": now}
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

    def create_access_token(self, user_id: int) -> str:
        return self._encode(
            {"sub": str(user_id), "type": "access"},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    async def create_refresh_token(self, user_id: int) -> Tuple[str, str]:
        jti = str(uuid.uuid4())

        token = self._encode(
        {"sub": str(user_id), "type": "refresh", "jti": jti},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return token, jti

    def decode_token(self, token: str, expected_type: str) -> tuple[str, Optional[str]]:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])

            sub = payload.get("sub")
            typ = payload.get("type")
            jti = payload.get("jti")
            if not sub or typ != expected_type:
                raise TokenError("Invalid token claims")
            try:
                sub = int(sub)
            except (ValueError, TypeError):
                pass  # если это email или uuid, оставим строкой

            return sub, jti
        except jwt.DecodeError as e:
            raise TokenError(str(e))
