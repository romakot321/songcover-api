from uuid import UUID

from src.task.domain.entities import TaskRun
from src.integration.domain.dtos import PlayHTStatus, PlayHTResponseDTO
from src.task.application.interfaces.task_runner import ITaskRunner
from src.integration.infrastructure.external_api.playht.adapter import PlayHTAdapter


class PlayHTTaskRunner[TResponseData: PlayHTResponseDTO](ITaskRunner):
    def __init__(self, adapter: PlayHTAdapter) -> None:
        self.adapter = adapter

    async def start(self, task_id: UUID, data: TaskRun) -> PlayHTResponseDTO:
        return await self.adapter.start_tts(task_id, data)

    async def get_result(self, task_id: UUID) -> PlayHTResponseDTO | None:
        result = await self.adapter.get_tts(task_id)
        if result and result.status in (PlayHTStatus.pending, PlayHTStatus.in_progress):
            return None
        return result
