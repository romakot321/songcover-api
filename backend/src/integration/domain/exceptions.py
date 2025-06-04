class IntegrationRunException(Exception):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message)
        self.message = message


class IntegrationRequestException(Exception):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message)
        self.message = message
