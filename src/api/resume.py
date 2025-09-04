
from fastapi import APIRouter, Depends, HTTPException

from src.logger import logger
from src.api.dependencies import get_current_user
from src.database import async_session_maker
from src.models.users import UsersOrm
from src.repositiries.resumes import ResumesRepository
from src.schemas.resumes import ReqAddResume, ResumePatch

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("")
async def add_resume(data: ReqAddResume, current_user: UsersOrm = Depends(get_current_user)):
    async with async_session_maker() as conn:
        logger.info("add_resume endpoint called")
        resume =  await ResumesRepository(conn).add_resume(user_id=current_user.id, resume_data=data)
        await conn.commit()
        return resume

@router.get("/me")
async def get_user_resumes(current_user: UsersOrm = Depends(get_current_user)):
    async with async_session_maker() as conn:
        logger.info("get_user_resumes endpoint called")
        result = await ResumesRepository(conn).get_filtered(user_id=current_user.id)
        return result

@router.get("/{resume_id}")
async def get_resume_by_id(resume_id: int, current_user: UsersOrm = Depends(get_current_user)):
    async with async_session_maker() as conn:
        logger.info("get_resume_by_id endpoint called")
        resume = await ResumesRepository(conn).get_one(id=resume_id)
        if not resume or resume.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        return resume


@router.patch("/{resume_id}")
async def update_resume(resume_id: int,
                        data: ResumePatch,
                        current_user: UsersOrm = Depends(get_current_user)
                        ):
    logger.info("update_resume endpoint called")
    async with async_session_maker() as conn:
        resume = await ResumesRepository(conn).get_one(id=resume_id)
        if not resume or resume.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")

        updated_resume = await ResumesRepository(conn).edit(id=resume_id, data=data)
        await conn.commit()
        return updated_resume

@router.patch("/{resume_id}/improve")
async def improve_resume(resume_id: int,
                         current_user: UsersOrm = Depends(get_current_user)):
    logger.info("improve_resume endpoint called")
    async with async_session_maker() as conn:
        resume = await ResumesRepository(conn).get_one(id=resume_id)
        if not resume or resume.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        return f"{resume.content} Improved"


@router.delete("{resume_id}")
async def delete_resume(resume_id: int,
                        current_user: UsersOrm = Depends(get_current_user)
                        ):
    logger.info("delete_resume endpoint called")
    async with async_session_maker() as conn:
        resume = await ResumesRepository(conn).get_one(id=resume_id)
        if not resume or resume.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        await ResumesRepository(conn).delete(id=resume_id)
        await conn.commit()
        return {"detail": "Ok"}





