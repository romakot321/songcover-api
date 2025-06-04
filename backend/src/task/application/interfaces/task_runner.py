import abc
from typing import Generic, TypeVar
from uuid import UUID

from src.task.domain.entities import TaskRun

TResponseData = TypeVar("TResponseData")


class ITaskRunner(abc.ABC, Generic[TResponseData]):
    @abc.abstractmethod
    async def start(self, task_id: UUID, data: TaskRun) -> TResponseData: ...

    @abc.abstractmethod
    async def get_result(self, task_id: UUID) -> TResponseData | None: ...
