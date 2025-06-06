from uuid import UUID

from loguru import logger
from pydantic import ValidationError
from src.core.config import settings
from src.integration.domain.dtos import TopMediaiSingerDTO
from src.integration.domain.exceptions import IntegrationRunException, IntegrationRequestException
from src.integration.infrastructure.http.api_client import HTTPApiClient
from src.integration.application.interfaces.result_storage import IResultStorage
from src.integration.infrastructure.external_api.topmediai.schemas import (
    TopMediaiWebSinger,
    TopMediaiCoverRequest,
    TopMediaiCoverResponse,
)


class TopMediaiAdapter:
    API_URL: str = "https://api.topmediai.com"
    API_TOKEN: str = settings.TOPMEDIAI_API_TOKEN

    def __init__(self, result_storage: IResultStorage):
        self.api_client = HTTPApiClient(self.API_URL, {"X-Api-Key": self.API_TOKEN})
        self.result_storage = result_storage

    async def get_singer_list(self) -> list[TopMediaiSingerDTO]:
        response = await self.api_client.request("GET", "/v1/singers")
        return [TopMediaiSingerDTO.model_validate(singer) for singer in response.get("Singers", [])]

    async def ai_cover(self, task_id: UUID, request: TopMediaiCoverRequest) -> TopMediaiCoverResponse:
        if request.youtube_url is None and request.file is None:
            raise TypeError("Empty youtube_url and file provided, no resource for generate")
        if request.file is not None:
            request.file.name = "audio.mp3"

        logger.info(f"Starting task {task_id}")
        response_raw = await self.api_client.request_form_data(
            "/v1/cover",
            fields=request.model_dump(exclude={"file", "tran"}),
            files={"file": request.file} if request.file else None,
        )

        try:
            response = TopMediaiCoverResponse.model_validate(response_raw)
        except ValidationError as e:
            raise IntegrationRunException(str(e)) from ValidationError

        self.result_storage.store("topmediai", str(task_id), response)
        logger.info(f"Finished task {task_id}. {response=}")

        return response

    async def web_list_singers(self, page_num: int, page_size: int) -> list[TopMediaiWebSinger]:
        response_raw = await self.api_client.http_client.get(
            "https://aicover-api.topmediai.com/v2/singer_list", params={"page_num": page_num, "page_size": page_size}
        )

        try:
            response = [TopMediaiWebSinger.model_validate(i) for i in response_raw.get("data", {}).get("data_list", [])]
        except ValidationError as e:
            raise IntegrationRequestException(str(e)) from ValidationError

        return response

    def get_ai_cover_result(self, task_id: UUID) -> TopMediaiCoverResponse | None:
        return self.result_storage.get("topmediai", str(task_id))
