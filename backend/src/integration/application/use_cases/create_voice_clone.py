from io import BytesIO

from loguru import logger
from fastapi import UploadFile, HTTPException

from src.integration.domain.dtos import PlayHTVoiceCloneReadDTO, PlayHTVoiceCloneCreateDTO
from src.integration.domain.exceptions import IntegrationRunException, IntegrationRequestException
from src.integration.infrastructure.external_api.playht.adapter import PlayHTAdapter


class CreateVoiceCloneUseCase:
    def __init__(self, adapter: PlayHTAdapter):
        self.adapter = adapter

    async def execute(self, audio: UploadFile, dto: PlayHTVoiceCloneCreateDTO) -> PlayHTVoiceCloneReadDTO:
        audio_buffer = BytesIO(await audio.read())
        try:
            result = await self.adapter.create_voice_clone(audio_buffer, dto.name)
        except IntegrationRunException as e:
            logger.error(e)
            raise HTTPException(400, detail=e.message)
        except IntegrationRequestException as e:
            logger.error(e)
            raise HTTPException(500, detail=e.message)

        return PlayHTVoiceCloneReadDTO(
            voice_id=result.id,
            name=result.name
        )
