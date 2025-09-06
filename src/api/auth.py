from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, HTTPException, Depends, Response, Cookie, Request
from fastapi.security import OAuth2PasswordRequestForm


from src.logger import logger
from src.api.dependencies import DBDep, UserDep
from src.config import settings

from src.schemas.jwt import TokenPair
from src.schemas.users import UserReqAdd, UserAdd, User, UserOut
from src.services.auth import AuthService, TokenError

router = APIRouter(prefix="/auth", tags=["Authorisation"])

REFRESH_COOKIE_NAME = "refresh_token"


def set_refresh_cookie(response: Response, value: str):
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=value,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )


def clear_refresh_cookie(response: Response):
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path="/",
    )


@router.post("/register")
async def register_user(db: DBDep, data: UserReqAdd):
    logger.info("register endpoint called")
    exist = await db.users.get_one_or_none(email=data.email)
    if exist:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )

    hashed_password = AuthService().hash_password(data.password)

    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    user = await db.users.add(new_user_data)
    await db.commit()
    return User.model_validate(user, from_attributes=True)


@router.post("/login")
async def login(
    db: DBDep, response: Response, form: OAuth2PasswordRequestForm = Depends()
):
    logger.info("Login endpoint called")
    user = await db.users.get_one(email=form.username)
    if not user or not AuthService().verify_password(
        form.password, user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access = AuthService().create_access_token(user_id=user.id)
    refresh, jti = AuthService().create_refresh_token(user.id)
    ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    qwe = datetime.now(timezone.utc) + timedelta(seconds=ttl)
    await db.jwt.add_refresh_token(id=jti, user_id=user.id, expires_at=qwe)
    await db.commit()

    set_refresh_cookie(response, refresh)
    return {"access_token": access, "token_type": "bearer"}


@router.post("/logout")
async def logout(
    db: DBDep,
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=REFRESH_COOKIE_NAME),
):
    if refresh_token:
        try:
            user_id, jti = AuthService().decode_token(
                refresh_token, expected_type="refresh"
            )
            if jti:
                await db.jwt.revoke_token(jti)
                await db.commit()
        except HTTPException:
            pass
        except TokenError:
            pass
    clear_refresh_cookie(response)
    return response.status_code


@router.post("/refresh", response_model=TokenPair)
async def refresh_token(db: DBDep, response: Response, request: Request):
    refresh = request.cookies.get(REFRESH_COOKIE_NAME)
    if not refresh:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    user_id, jti = AuthService().verify_refresh_token(refresh)

    new_access = AuthService().create_access_token(user_id)
    new_refresh, new_jti = AuthService().create_refresh_token(user_id)

    ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl)

    await db.jwt.revoke_token(jti)
    await db.jwt.add_refresh_token(id=new_jti, user_id=user_id, expires_at=expires_at)
    await db.commit()

    set_refresh_cookie(response, new_refresh)
    return TokenPair(access_token=new_access, refresh_token=new_refresh)


@router.get("/me", response_model=UserOut)
async def me(current_user: UserDep):
    return UserOut(id=current_user.id, email=current_user.email)
