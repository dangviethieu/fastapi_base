from typing import Any, Optional
from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: str

class BaseResponse(StatusResponse):
    content: Any

class IdString(BaseModel):
    id: str

    class Config:
        orm_mode = True

class BaseIdResponse(StatusResponse):
    content: Optional[IdString]

class ErrorResponse(BaseModel):
    error: str

class ResAccessToken(BaseModel):
    accessToken: str

class ResBaseLogin(ResAccessToken):
    refreshToken: str

class ResRefreshToken(StatusResponse):
    content: Optional[ResAccessToken]
