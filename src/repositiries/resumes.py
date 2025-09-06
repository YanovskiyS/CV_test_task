from sqlalchemy import insert

from src.repositiries.base import BaseRepository
from src.models.resumes import ResumesOrm
from src.schemas.resumes import Resume, AddResume, ReqAddResume


class ResumesRepository(BaseRepository):
    model = ResumesOrm
    schema = Resume

    async def add_resume(self, user_id: int, resume_data: ReqAddResume):
        resume_data = AddResume(user_id=user_id, **resume_data.model_dump())
        add_resume_stmt = (
            insert(self.model).values(**resume_data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_resume_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)
