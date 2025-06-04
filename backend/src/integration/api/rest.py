from fastapi import APIRouter, Depends, File, UploadFile

from src.integration.application.use_cases.get_voices_list import GetVoicesListUseCase
from src.integration.domain.dtos import TopMediaiSingerDTO
from src.integration.api.dependencies import PlayHTAdapterDepend, TopMediaiAdapterDepend
from src.integration.application.use_cases.create_voice_clone import (
    CreateVoiceCloneUseCase,
)
from src.integration.domain.dtos import (
    PlayHTVoiceCloneCreateDTO,
    PlayHTVoiceCloneReadDTO,
)


router = APIRouter()


@router.post("/playht/voice", response_model=PlayHTVoiceCloneReadDTO, include_in_schema=False)
async def create_voice_clone(
    adapter: PlayHTAdapterDepend,
    audio: UploadFile = File(),
    data: PlayHTVoiceCloneCreateDTO = Depends(),
):
    """The audio file selected as the source for the voice clone should have a duration ranging from 2 seconds to 1 hour. It can be in any audio format, as long as it falls within the size range of 5kb to 50 MB."""
    return await CreateVoiceCloneUseCase(adapter).execute(audio, data)


@router.get("/topmediai/voice", response_model=list[TopMediaiSingerDTO])
async def get_voice_list(adapter: TopMediaiAdapterDepend):
    return await GetVoicesListUseCase(adapter).execute()
