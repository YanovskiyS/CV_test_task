from sqlalchemy import select, update

from src.models.jwt import RefreshTokensOrm
from src.repositiries.base import BaseRepository
from src.schemas.jwt import TokenPair


class JwtRepository(BaseRepository):
    model = RefreshTokensOrm
    schema = TokenPair

    async def add_refresh_token(
        self, id: str, user_id: int, expires_at, revoked: bool = False
    ):
        token = RefreshTokensOrm(
            id=id,
            user_id=user_id,
            expires_at=expires_at,
            revoked=revoked,
        )
        self.session.add(token)
        return token

    async def get_token_by_id(self, token_id: str):
        stmt = select(RefreshTokensOrm).where(RefreshTokensOrm.id == token_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke_token(self, token_id: str):
        stmt = (
            update(RefreshTokensOrm)
            .where(RefreshTokensOrm.id == token_id)
            .values(revoked=True)
        )
        await self.session.execute(stmt)
