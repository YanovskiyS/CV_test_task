from typing import Optional

from pydantic import BaseModel, Field


class ReqAddResume(BaseModel):
    title: str = Field(...)
    content: Optional[str] = None

class Resume(ReqAddResume):
    id: int

class AddResume(ReqAddResume):
    user_id: int


class ResumePatch(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None