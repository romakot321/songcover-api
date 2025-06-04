from typing import Annotated

from fastapi import Depends
from src.integration.infrastructure.external_api.topmediai.adapter import TopMediaiAdapter
from src.integration.infrastructure.external_api.topmediai.runner import TopMediaiTaskRunner
from src.integration.infrastructure.external_api.playht.adapter import PlayHTAdapter
from src.integration.infrastructure.external_api.playht.runner import PlayHTTaskRunner
from src.integration.infrastructure.http.client import HTTPClient
from src.integration.infrastructure.result_storage import InMemoryResultStorage
from src.task.application.interfaces.task_runner import ITaskRunner


def get_playht_adapter() -> PlayHTAdapter:
    return PlayHTAdapter(HTTPClient(), InMemoryResultStorage())


def get_playht_task_runner() -> ITaskRunner:
    adapter = get_playht_adapter()
    return PlayHTTaskRunner(adapter)


def get_topmediai_adapter() -> TopMediaiAdapter:
    return TopMediaiAdapter(InMemoryResultStorage())


def get_topmediai_task_runner() -> ITaskRunner:
    adapter = get_topmediai_adapter()
    return TopMediaiTaskRunner(adapter)


PlayHTAdapterDepend = Annotated[PlayHTAdapter, Depends(get_playht_adapter)]
TopMediaiAdapterDepend = Annotated[TopMediaiAdapter, Depends(get_topmediai_adapter)]
