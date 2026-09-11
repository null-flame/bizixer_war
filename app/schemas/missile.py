from pydantic import ConfigDict
from sqlmodel import SQLModel

from app.models.enums import Front, TType

class buy_missile_In(SQLModel):
    missile_type: TType
    count: int
class buy_missile_out(SQLModel):
    message: str
    coin: int
class attack_In(SQLModel):
    Tid: int
    missile_type: TType
    factory_type: TType
    count: int
class attack_out(SQLModel):
    meesage: str