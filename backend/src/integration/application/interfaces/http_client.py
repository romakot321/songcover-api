import abc


class IHTTPClient(abc.ABC):
    @abc.abstractmethod
    async def post(
        self,
        url: str,
        json: dict | None = None,
        headers: dict | None = None,
        form: dict | None = None,
        data: str | bytes | None = None,
        **kwargs
    ) -> dict: ...

    @abc.abstractmethod
    async def get(
        self, url: str, params: dict | None = None, headers: dict | None = None, **kwargs
    ) -> dict: ...
