from pydantic import BaseModel


class Log(BaseModel):
    message: str
    datetime: str
    service: str


class StreamObject(BaseModel):
    id_: str
    log: Log
