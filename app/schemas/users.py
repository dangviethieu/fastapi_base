from typing import List, Optional
from pydantic import BaseModel, validator

from app.schemas.base import StatusResponse, ResBaseLogin


class ReqCreateUser(BaseModel):
    email: str = None
    fullName: str = None
    roleId: int = None
    phone: str = None
    password: str = None

    class Config:
        orm_mode = True

class ResBaseUserInfo(BaseModel):
    id: str
    email: str = None
    fullName: str = None
    interfaceLanguageCode: str = None
    uniqueId: str = None
    phone: str = None

class UserOnCreateObj(ResBaseLogin):
    userInfo: Optional[ResBaseUserInfo]

class ResUserCreate(StatusResponse):
    content: Optional[UserOnCreateObj]

class ReqLoginUser(BaseModel):
    email: str
    password: str

class ResAddressObj(BaseModel):
    id: int
    name: str = None
    streetAndNumber: str = None
    country: str = None
    city: str = None
    zip: str = None

    class Config:
        orm_mode = True

class ResUserInfoObj(ResBaseUserInfo):
    address: Optional[ResAddressObj]

class ResUserLoginObj(ResBaseLogin):
    userInfo: Optional[ResUserInfoObj]

class ResUserAccessToken(StatusResponse):
    content: Optional[ResUserLoginObj]
 
    