from src.models.users import UsersOrm
from src.repositiries.base import BaseRepository
from src.schemas.users import User


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User