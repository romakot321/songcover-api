from src.integration.infrastructure.external_api.playht.schemas import PlayHTTTSRequestJobSchema, PlayHTTTSRequestSchema
from src.task.domain.entities import TaskRun


class DomainToRequestMapper:
    def map_one(self, data: TaskRun) -> PlayHTTTSRequestSchema:
        return PlayHTTTSRequestSchema(
            webhook_url=None,
            jobs=[
                PlayHTTTSRequestJobSchema(**data.model_dump())
            ]
        )
