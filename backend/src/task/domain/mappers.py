from src.integration.domain.dtos import PlayHTResponseDTO, PlayHTStatus
from src.task.application.interfaces.task_runner import TResponseData
from src.task.domain.dtos import TaskResultDTO
from src.task.domain.entities import TaskSource, TaskStatus


class IntegrationResponseToDomainMapper:
    def __init__(self, source: TaskSource | None = None) -> None:
        self.source = source

    def map_one(self, data: TResponseData) -> TaskResultDTO:
        self.source = self._define_source(data)

        if self.source == TaskSource.playht:
            return PlayHTResponseToDomainMapper().map_one(data)

        raise ValueError("Failed to map integration response: Unknown data source")

    def _define_source(self, data: TResponseData) -> TaskSource | None:
        if hasattr(data, "status") and hasattr(data, "output"):
            return TaskSource.playht


class PlayHTResponseToDomainMapper:
    def map_one(self, data: PlayHTResponseDTO) -> TaskResultDTO:
        return TaskResultDTO(
            status=self._map_playht_status(data.status),
            result=data.output.url if data.output else None,
            error=data.model_dump_json() if data.status == PlayHTStatus.failed else None
        )

    def _map_playht_status(self, status: PlayHTStatus) -> TaskStatus:
        if status == PlayHTStatus.pending:
            return TaskStatus.queued
        if status == PlayHTStatus.in_progress:
            return TaskStatus.started
        if status == PlayHTStatus.completed:
            return TaskStatus.finished
        if status == PlayHTStatus.failed:
            return TaskStatus.failed
