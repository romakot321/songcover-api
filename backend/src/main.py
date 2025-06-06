from fastapi import FastAPI

from src.integration.api.rest import router as integration_router
from src.task.api.rest import router as task_router
import src.core.logging_setup
from src.core.logging_setup import setup_fastapi_logging

app = FastAPI(title="Song Cover API")

app.include_router(task_router, tags=["Task"], prefix="/api/task")
app.include_router(integration_router, tags=["Integration"], prefix="/api/integration")

setup_fastapi_logging(app)
