from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


from src.database import async_session_maker
from src.models.users import UsersOrm
from src.repositiries.users import UsersRepository
from src.services.auth import AuthService, TokenError
from src.utils.db_manager import DBManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),

) -> UsersOrm:
    try:
        user_id, _ = AuthService().decode_token(token, expected_type="access")
    except TokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token")
    async with async_session_maker() as conn:
        user= await UsersRepository(conn).get_one(id=user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user

UserIdDep = Annotated[UsersOrm, Depends(get_current_user)]

def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
