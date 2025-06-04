import abc
from typing import Any


class IResultStorage(abc.ABC):
    @abc.abstractmethod
    def store(self, source: str, task_id: str, result: Any): ...

    @abc.abstractmethod
    def get(self, source: str, task_id: str) -> Any | None: ...
