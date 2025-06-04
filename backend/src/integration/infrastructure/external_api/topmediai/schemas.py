from io import BytesIO
from pydantic import BaseModel, ConfigDict


class TopMediaiCoverRequest(BaseModel):
    singer_id: int
    file: BytesIO | None = None
    youtube_url: str | None = None
    tran: int = 0

    model_config = ConfigDict(arbitrary_types_allowed=True)


class TopMediaiCoverResponse(BaseModel):
    class Data(BaseModel):
        combine_file: str
        filename: str
        uuid: str

    status: int
    message: str
    data: Data
