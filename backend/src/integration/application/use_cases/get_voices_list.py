from src.integration.domain.dtos import TopMediaiSingerDTO
from src.integration.infrastructure.external_api.topmediai.adapter import TopMediaiAdapter


class GetVoicesListUseCase:
    def __init__(self, adapter: TopMediaiAdapter) -> None:
        self.adapter = adapter

    async def execute(self) -> list[TopMediaiSingerDTO]:
        return await self.adapter.get_singer_list()
