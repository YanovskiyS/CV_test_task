from src.repositiries.resumes import ResumesRepository
from src.repositiries.jwt import JwtRepository
from src.repositiries.users import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.resumes = ResumesRepository(self.session)
        self.jwt = JwtRepository(self.session)
        self.users = UsersRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
