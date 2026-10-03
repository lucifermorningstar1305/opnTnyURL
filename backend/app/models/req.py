from pydantic import BaseModel, HttpUrl


class AddUrlRequest(BaseModel):
    url: HttpUrl
