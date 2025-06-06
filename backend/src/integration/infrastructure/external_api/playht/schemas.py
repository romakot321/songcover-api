from io import BytesIO
from typing import Literal

from pydantic import BaseModel, ConfigDict


class PlayHTTTSRequestJobSchema(BaseModel):
    custom_id: str | None = None
    webhook_url: str | None = None
    voice_engine: str = "PlayDialog"
    voice: str | None = None
    text: str | None = None
    quality: str | None = None
    output_format: str = "mp3"
    speed: float | None = None
    sample_rate: int | None = None
    seed: int | None = None
    temperature: float | None = None
    language: str | None = None
    voice_2: str | None = None


class PlayHTTTSRequestSchema(BaseModel):
    webhook_url: str | None = None
    jobs: list[PlayHTTTSRequestJobSchema]


class PlayHTTTSResponseSchema(BaseModel):
    id: str
    status: str
    webhook_url: str | None = None
    jobs: list[PlayHTTTSRequestJobSchema]


class PlayHTVoiceCloneRequestSchema(BaseModel):
    voice_name: str
    sample_file: BytesIO

    model_config = ConfigDict(arbitrary_types_allowed=True)


class PlayHTVoiceCloneResponseSchema(BaseModel):
    id: str
    name: str
    type: Literal["high-fidelity", "instant"]
