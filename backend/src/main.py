from fastapi import FastAPI

from src.integration.api.rest import router as integration_router
from src.task.api.rest import router as task_router

app = FastAPI(title="Song Cover API")

app.include_router(task_router, tags=["Task"], prefix="/api/task")
app.include_router(integration_router, tags=["Integration"], prefix="/api/integration")
