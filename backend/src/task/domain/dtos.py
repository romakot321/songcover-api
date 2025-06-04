from uuid import UUID
from pydantic import BaseModel

from src.task.domain.entities import TaskStatus


class TaskCreateDTO(BaseModel):
    user_id: str
    app_bundle: str
    voice_id: int
    youtube_url: str | None = None


class TaskReadDTO(BaseModel):
    id: UUID
    status: TaskStatus
    result: str | None = None
    error: str | None = None


class TaskResultDTO(BaseModel):
    status: TaskStatus
    result: str | None = None
    error: str | None = None
