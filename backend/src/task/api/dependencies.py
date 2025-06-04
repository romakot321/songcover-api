from typing import Annotated

from fastapi import Depends
from src.integration.api.dependencies import get_topmediai_task_runner
from src.task.application.interfaces.task_runner import ITaskRunner
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.infrastructure.db.unit_of_work import TaskUnitOfWork


def get_task_uow() -> ITaskUnitOfWork:
    return TaskUnitOfWork()


TaskUoWDepend = Annotated[ITaskUnitOfWork, Depends(get_task_uow)]
TaskRunnerDepend = Annotated[ITaskRunner, Depends(get_topmediai_task_runner)]
