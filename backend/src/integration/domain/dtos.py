from enum import Enum

from pydantic import Field, BaseModel


class GetListParamsDTO(BaseModel):
    page: int = Field(gt=0, default=1)
    count: int = 50


class PlayHTStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class PlayHTOutput(BaseModel):
    duration: int
    size: int
    url: str


class PlayHTResponseDTO(BaseModel):
    id: str
    status: PlayHTStatus
    output: PlayHTOutput | None = None


class PlayHTVoiceCloneCreateDTO(BaseModel):
    name: str


class PlayHTVoiceCloneReadDTO(BaseModel):
    voice_id: str
    name: str


class TopMediaiSingerDTO(BaseModel):
    singer_name: str
    singer_id: int
    singer_avatar_preview: str | None = None
    singer_audio_preview: str | None = None


class TopMediaiResponseDTO(BaseModel):
    status: int
    message: str | None = None
    combine_file: str | None = None


class TopMediaiRequestDTO(BaseModel):
    voice_id: int
    youtube_url: str | None = None


IntegrationTaskRunParamsDTO = TopMediaiRequestDTO

