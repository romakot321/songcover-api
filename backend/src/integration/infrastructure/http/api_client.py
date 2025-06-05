from io import BytesIO
from loguru import logger
from typing import Literal
from src.integration.application.interfaces.http_api_client import (
    IHTTPApiClient,
)
from src.integration.application.interfaces.http_client import IHTTPClient
from src.integration.infrastructure.http.client import HTTPClient


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

        boundary = "------geckoformboundarya959ea91fc1c4a8615ee517e14d6ffc5"
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        data = self.encode_multipart_formdata(boundary, fields, files)

        response = await self.http_client.post(
            url, params=params, headers=headers, data=data
        )

        return response

    @staticmethod
    def encode_multipart_formdata(BOUNDARY, fields, files):
        CRLF = '\r\n'.encode('utf-8')
        L = []
        for (key, value) in fields.items():
            if value is None:
                value = ""
            L.append(('--' + BOUNDARY).encode('utf-8'))
            L.append(('Content-Disposition: form-data; name="%s"' % key).encode('utf-8'))
            L.append(''.encode('utf-8'))
            L.append(str(value).encode('utf-8'))
        for (key, value) in files.items():
            L.append(('--' + BOUNDARY).encode('utf-8'))
            L.append(('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, "file.mp3")).encode('utf-8'))
            L.append(('Content-Type: %s' % "audio/mpeg").encode('utf-8'))
            L.append(''.encode('utf-8'))
            L.append(value.read())
        L.append(('--' + BOUNDARY + '--').encode('utf-8'))
        L.append(''.encode('utf-8'))
        body = CRLF.join(L)
        return body
