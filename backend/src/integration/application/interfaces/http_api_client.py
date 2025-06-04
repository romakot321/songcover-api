import abc
from io import BytesIO
from typing import Literal


class IHTTPApiClient(abc.ABC):
    @abc.abstractmethod
    async def request(
        self,
        method: Literal["GET", "POST"],
        endpoint: str,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> dict: ...

    @abc.abstractmethod
    async def request_form_data(
        self,
        endpoint: str,
        fields: dict | None = None,
        files: dict[str, BytesIO] | None = None,
        headers: dict | None = None,
        params: dict | None = None,
    ) -> dict: ...
