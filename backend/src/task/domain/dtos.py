from uuid import UUID
from fastapi import Form
from pydantic import BaseModel

from src.task.domain.entities import TaskStatus


class TaskCreateDTO(BaseModel):
    user_id: str
    app_bundle: str
    voice_id: int
    youtube_url: str | None = None

    @classmethod
    def as_form(
        cls,
        user_id: str = Form(),
        app_bundle: str = Form(),
        voice_id: int = Form(),
        youtube_url: str | None = Form(None),
    ):
        return cls(
            user_id=user_id,
            app_bundle=app_bundle,
            voice_id=voice_id,
            youtube_url=youtube_url,
        )


class TaskReadDTO(BaseModel):
    id: UUID
    status: TaskStatus
    result: str | None = None
    error: str | None = None


class TaskResultDTO(BaseModel):
    status: TaskStatus
    result: str | None = None
    error: str | None = None
