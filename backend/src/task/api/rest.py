from io import BytesIO
from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, UploadFile

from src.task.api.dependencies import TaskRunnerDepend, TaskUoWDepend
from src.task.application.use_cases.create_task import CreateTaskUseCase
from src.task.application.use_cases.get_task import GetTaskUseCase
from src.task.application.use_cases.run_task import RunTaskUseCase
from src.task.domain.dtos import TaskCreateDTO, TaskReadDTO


router = APIRouter()


@router.post("", response_model=TaskReadDTO)
async def create_and_run_task(
    data: TaskCreateDTO,
    music: UploadFile | None,
    uow: TaskUoWDepend,
    runner: TaskRunnerDepend,
    background_tasks: BackgroundTasks,
):
    task = await CreateTaskUseCase(uow).execute(data)
    if music is not None:
        music = BytesIO(await music.read())
    background_tasks.add_task(RunTaskUseCase(uow, runner).execute, task.id, data, music)
    return task


@router.get("/{task_id}", response_model=TaskReadDTO)
async def get_task(task_id: UUID, uow: TaskUoWDepend):
    return await GetTaskUseCase(uow).execute(task_id)
