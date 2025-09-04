from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.config import settings
from src.database import async_session_maker_null_pool, engine_null_pool, Base
from src.main import app
from src.utils.db_manager import DBManager


async def get_db_nul_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_nul_pool():
        yield db


app.dependency_overrides[get_db] = get_db_nul_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


async def register_and_login(ac):
    # 1. Регистрация
    await ac.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )

    # 2. Логин
    login_res = await ac.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


