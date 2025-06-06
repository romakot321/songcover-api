from src.task.domain.entities import TaskRun
from src.integration.infrastructure.external_api.playht.schemas import PlayHTTTSRequestSchema, PlayHTTTSRequestJobSchema


class DomainToRequestMapper:
    def map_one(self, data: TaskRun) -> PlayHTTTSRequestSchema:
        return PlayHTTTSRequestSchema(
            webhook_url=None,
            jobs=[
                PlayHTTTSRequestJobSchema(**data.model_dump())
            ]
        )
