import asyncio
from uuid import UUID

from src.integration.infrastructure.external_api.topmediai.schemas import TopMediaiCoverRequest, TopMediaiCoverResponse
from src.task.domain.entities import TaskRun
from src.integration.infrastructure.external_api.topmediai.adapter import TopMediaiAdapter
from src.task.application.interfaces.task_runner import ITaskRunner


class TopMediaiTaskRunner[TResponseData: TopMediaiCoverResponse](ITaskRunner):
    def __init__(self, adapter: TopMediaiAdapter) -> None:
        self.adapter = adapter

    async def start(self, task_id: UUID, data: TaskRun) -> TopMediaiCoverResponse:
        request = TopMediaiCoverRequest(singer_id=data.voice_id, file=data.audio, youtube_url=data.youtube_url)
        asyncio.create_task(self.adapter.ai_cover(task_id, request))
        response = TopMediaiCoverResponse(status=0, message="", data=TopMediaiCoverResponse.Data(combine_file="", filename="", uuid=""))
        return response

    async def get_result(self, task_id: UUID) -> TopMediaiCoverResponse | None:
        return self.adapter.get_ai_cover_result(task_id)
