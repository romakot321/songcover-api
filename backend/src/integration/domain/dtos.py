from enum import Enum
from pydantic import BaseModel


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


class TopMediaiResponseDTO(BaseModel):
    status: int
    message: str | None = None
    combine_file: str | None = None
