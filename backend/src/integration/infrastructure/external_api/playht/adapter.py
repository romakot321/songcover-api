from io import BytesIO
from uuid import UUID

from pydantic import ValidationError
from src.integration.application.interfaces.http_client import IHTTPClient
from src.integration.application.interfaces.result_storage import IResultStorage
from src.integration.domain.dtos import PlayHTResponseDTO, PlayHTStatus
from src.integration.domain.exceptions import IntegrationRunException
from src.integration.infrastructure.external_api.playht.mappers import (
    DomainToRequestMapper,
)
from src.integration.infrastructure.external_api.playht.schemas import (
    PlayHTTTSResponseSchema,
    PlayHTVoiceCloneResponseSchema,
)
from src.task.domain.entities import TaskRun
from src.core.config import settings


_etasykanerabotaetkaknapisanovdokymentatsiiidinaxyi = """------geckoformboundaryd826725fddca988df034dfc9ef767104
Content-Disposition: form-data; name="sample_file"; filename="bul_fvo_ralicam_ivr.mp3"
Content-Type: audio/mpeg

{sample_file}
------geckoformboundaryd826725fddca988df034dfc9ef767104
Content-Disposition: form-data; name="voice_name"

{voice_name}
------geckoformboundaryd826725fddca988df034dfc9ef767104--"""


class PlayHTAdapter:
    API_URL: str = "https://api.play.ht"
    API_TOKEN: str = settings.PLAYHT_API_TOKEN
    API_USER_ID: str = settings.PLAYHT_API_USER_ID

    def __init__(
        self, http_client: IHTTPClient, result_storage: IResultStorage
    ) -> None:
        self.http_client = http_client
        self.result_storage = result_storage
        self.auth_headers = {
            "AUTHORIZATION": self.API_TOKEN,
            "X-USER-ID": self.API_USER_ID,
            "accept": "application/json",
        }

    async def start_tts(self, task_id: UUID, data: TaskRun) -> PlayHTResponseDTO:
        request = DomainToRequestMapper().map_one(data)
        request.jobs[0].custom_id = str(task_id)[:30]
        response = await self.http_client.post(
            self.API_URL + "/api/v2/tts/batches",
            json=request.model_dump(exclude_none=True),
            headers=self.auth_headers,
        )
        try:
            response_schema = PlayHTTTSResponseSchema.model_validate(response)
        except ValidationError as e:
            raise IntegrationRunException(str(e))
        self.result_storage.store("playht", str(task_id), response_schema)
        return PlayHTResponseDTO(
            **response_schema.jobs[0].model_dump(),
            id=response_schema.jobs[0].custom_id,
            status=response_schema.status,
        )

    async def get_tts(self, task_id: UUID) -> PlayHTResponseDTO | None:
        result = self.result_storage.get("playht", str(task_id))
        response_dto = None

        if isinstance(result, PlayHTTTSResponseSchema):
            response = await self.http_client.get(
                self.API_URL
                + f"/api/v2/tts/batches/{result.id}/job/custom-id/{str(task_id)[:30]}",
                headers=self.auth_headers,
            )
            response_dto = PlayHTResponseDTO.model_validate(response)
            if response_dto.status in (PlayHTStatus.completed, PlayHTStatus.failed):
                self.result_storage.store("playht", str(task_id), response_dto)
        elif isinstance(result, PlayHTResponseDTO):
            response_dto = result

        return response_dto

    async def create_voice_clone(
        self, file: BytesIO, voice_name: str
    ) -> PlayHTVoiceCloneResponseSchema:
        import requests

        url = "https://api.play.ht/api/v2/cloned-voices/instant"

        files = {"sample_file": ("bul_fvo_ralicam_ivr.mp3", file, "audio/mpeg")}
        payload = {"voice_name": voice_name}
        headers = {
            "accept": "application/json",
            "AUTHORIZATION": self.API_TOKEN,
            "X-USER-ID": self.API_USER_ID,
        }

        response = requests.post(url, data=payload, files=files, headers=headers).json()

        try:
            response_schema = PlayHTVoiceCloneResponseSchema.model_validate(response)
        except ValidationError as e:
            raise IntegrationRunException(str(e))

        return response_schema
