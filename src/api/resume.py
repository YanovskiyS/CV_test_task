from fastapi import APIRouter, HTTPException

from src.logger import logger
from src.api.dependencies import DBDep, UserDep
from src.schemas.resumes import ReqAddResume, ResumePatch

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("")
async def add_resume(db: DBDep, data: ReqAddResume, current_user: UserDep):
    logger.info("add_resume endpoint called")
    resume = await db.resumes.add_resume(user_id=current_user.id, resume_data=data)
    await db.commit()
    return resume


@router.get("/me")
async def get_user_resumes(db: DBDep, current_user: UserDep):
    logger.info("get_user_resumes endpoint called")
    result = await db.resumes.get_filtered(user_id=current_user.id)
    return result


@router.get("/{resume_id}")
async def get_resume_by_id(db: DBDep, resume_id: int, current_user: UserDep):
    logger.info("get_resume_by_id endpoint called")
    resume = await db.resumes.get_one(id=resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return resume


@router.patch("/{resume_id}")
async def update_resume(
    db: DBDep, resume_id: int, data: ResumePatch, current_user: UserDep
):
    logger.info("update_resume endpoint called")
    resume = await db.resumes.get_one(id=resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    updated_resume = await db.resumes.edit(id=resume_id, data=data)
    await db.commit()
    return updated_resume


@router.patch("/{resume_id}/improve")
async def improve_resume(db: DBDep, resume_id: int, current_user: UserDep):
    logger.info("improve_resume endpoint called")
    resume = await db.resumes.get_one(id=resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return f"{resume.content} Improved"


@router.delete("/{resume_id}")
async def delete_resume(db: DBDep, resume_id: int, current_user: UserDep):
    logger.info("delete_resume endpoint called")
    resume = await db.resumes.get_one(id=resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    await db.resumes.delete(id=resume_id)
    await db.commit()
    return {"detail": "Ok"}
