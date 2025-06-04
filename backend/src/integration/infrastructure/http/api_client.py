from io import BytesIO
from typing import Literal
from backend.src.integration.application.interfaces.http_api_client import (
    IHTTPApiClient,
)
from backend.src.integration.application.interfaces.http_client import IHTTPClient
from backend.src.integration.infrastructure.http.client import HTTPClient


class HTTPApiClient(IHTTPApiClient):
    def __init__(
        self,
        api_url: str,
        auth_header: dict[str, str] | None = None,
        http_client: IHTTPClient = HTTPClient(),
    ) -> None:
        self.api_url = api_url.rstrip("/")
        self.http_client = http_client
        self.auth_header = auth_header

    async def request(
        self,
        method: Literal["GET", "POST"],
        endpoint: str,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        form: dict | None = None,
        data: str | bytes | None = None,
    ) -> dict:
        if self.auth_header and list(self.auth_header.keys())[0] not in (headers or {}):
            headers = (headers or {}) | self.auth_header
        url = self.api_url + "/" + endpoint.lstrip("/")

        func = getattr(self.http_client, method.lower())
        response = await func(
            url=url, json=json, params=params, headers=headers, form=form, data=data
        )

        return response

    async def request_form_data(
        self,
        endpoint: str,
        fields: dict | None = None,
        files: dict[str, BytesIO] | None = None,
        headers: dict | None = None,
        params: dict | None = None,
    ) -> dict:
        if headers is None:
            headers = {}
        if self.auth_header and list(self.auth_header.keys())[0] not in headers:
            headers |= self.auth_header
        url = self.api_url + "/" + endpoint.lstrip("/")

        boundary = "-----------------------------9051914041544843365972754266"
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        data = self.prepare_form_data(boundary, fields, files)

        response = await self.http_client.post(
            url, params=params, headers=headers, data=data
        )

        return response

    @staticmethod
    def prepare_form_data(
        boundary: str,
        fields: dict | None = None,
        files: dict[str, BytesIO] | None = None,
    ) -> str:
        data = ""

        for key, value in (fields or {}).items():
            data += (
                f"{boundary}\r\n"
                f'Content-Disposition: form-data; name="{key}"\r\n'
                "\r\n"
                f"{value}\r\n"
            )
        for key, file in (files or {}).items():
            file_body = file.getvalue().decode("latin-1")
            data += (
                f"{boundary}\r\n"
                f'Content-Disposition: form-data; name="{key}"; filename="{file.name or "file.mp3"}"\r\n'
                "\r\n"
                f"{file_body}\r\n"
            )

        data += f"{boundary}--\r\n"

        return data
