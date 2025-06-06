from src.integration.domain.dtos import GetListParamsDTO, TopMediaiSingerDTO
from src.integration.infrastructure.external_api.topmediai.adapter import TopMediaiAdapter
from src.integration.infrastructure.external_api.topmediai.schemas import TopMediaiWebSinger


class GetVoicesListUseCase:
    def __init__(self, adapter: TopMediaiAdapter) -> None:
        self.adapter = adapter

    async def execute(self, params: GetListParamsDTO) -> list[TopMediaiSingerDTO]:
        singers = await self.adapter.web_list_singers(params.page, params.count)
        return [
            self._map_singer(singer)
            for singer in singers
        ]

    @staticmethod
    def _map_singer(singer: TopMediaiWebSinger) -> TopMediaiSingerDTO:
        return TopMediaiSingerDTO(
            singer_name=singer.display_name,
            singer_id=singer.id,
            singer_avatar_preview=singer.portrait,
            singer_audio_preview=singer.audition[0] if singer.audition else None
        )
