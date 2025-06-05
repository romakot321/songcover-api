from loguru import logger
from src.core.config import settings


def add_custom_fields(record):
    record["extra"]["app_name"] = settings.PROJECT_NAME
    return True


logger.add("/app/logs/app.json", format="{time:MMMM D, YYYY > HH:mm:ss!UTC} | {level} | {message}", serialize=True, rotation="500 MB", filter=add_custom_fields)
