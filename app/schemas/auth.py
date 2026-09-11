from pydantic import ConfigDict
from sqlmodel import SQLModel

from app.models.enums import Front, TType


class get_coin_out(SQLModel):
    message: str
    coin: int


class BuyFactoryI(SQLModel):
    factory_type: TType
    count: int


class BuyFactoryO(SQLModel):
    message: str
    coin: int


class UserI(SQLModel):
    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)
    username: str
    password: str
    front: Front


class UserO(SQLModel):
    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)
    id: int
    username: str
    front: Front


class UserLoginI(SQLModel):
    username: str
    password: str
