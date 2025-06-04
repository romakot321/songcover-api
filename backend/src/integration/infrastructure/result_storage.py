from typing import Any
from src.integration.application.interfaces.result_storage import IResultStorage

_storage = {}


class InMemoryResultStorage(IResultStorage):
    def __init__(self) -> None:
        global _storage
        self.storage: dict[str, dict[str, Any]] = _storage

    def store(self, source: str, task_id: str, result: Any):
        if source not in self.storage:
            self.storage[source] = {}
        self.storage[source][task_id] = result

    def get(self, source: str, task_id: str) -> Any | None:
        return self.storage.get(source, {}).get(task_id)
