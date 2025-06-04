from enum import Enum
from io import BytesIO
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class TaskSource(str, Enum):
    playht = "playht"
    topmediai = "topmediai"


class TaskStatus(str, Enum):
    queued = "queued"
    started = "started"
    failed = "failed"
    finished = "finished"


class Task(BaseModel):
    id: UUID
    user_id: str
    app_bundle: str
    status: TaskStatus
    result: str | None = None
    error: str | None = None


class TaskCreate(BaseModel):
    user_id: str
    app_bundle: str


class TaskResultQuality(str, Enum):
    draft = 'draft'
    low = 'low'
    medium = 'medium'
    high = 'high'
    premium = 'premium'


class TaskRun(BaseModel):
    voice_id: int
    youtube_url: str | None = None
    audio: BytesIO | None = None

#    text: str
#    voice: str | None = None
#    quality: TaskResultQuality = TaskResultQuality.draft
#    speed: float | None = Field(ge=0.1, le=5.0, default=None)
#    sample_rate: int | None = Field(ge=8000, le=48000)
#    seed: int | None = Field(ge=0, default=None)
#    temperature: float | None = Field(ge=0, le=2, default = None)
#    language: str | None = "english"
#    voice_2: str | None = Field(description="For dialogs", default=None)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class TaskUpdate(BaseModel):
    status: TaskStatus | None = None
    result: str | None = None
    error: str | None = None

