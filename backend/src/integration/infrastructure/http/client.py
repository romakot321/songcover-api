import aiohttp

from src.integration.domain.exceptions import IntegrationRequestException
from src.integration.application.interfaces.http_client import IHTTPClient


class HTTPClient(IHTTPClient):
    async def post(
        self,
        url: str,
        json: dict | None = None,
        headers: dict | None = None,
        form: dict | None = None,
        data: str | aiohttp.FormData | bytes | None = None,
        **kwargs,
    ) -> dict:
        async with aiohttp.ClientSession() as session:
            response = await session.post(url, json=json, headers=headers, data=data)
            if not response.ok:
                raise IntegrationRequestException(await response.text())
            body = await response.json()

        return body

    async def get(
        self,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        **kwargs,
    ) -> dict:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, params=params, headers=headers)
            if not response.ok:
                raise IntegrationRequestException(await response.text())
            body = await response.json()
        return body
