from pydantic import ConfigDict
from sqlmodel import SQLModel
from typing import Optional
from app.models.enums import Front, TType
from datetime import datetime, timezone, timedelta

class Queue_IO(SQLModel):
    id: int
    count: int
    model: TType
    ready_at: datetime

class UserIO(SQLModel):
    id: int
    username: str
    front: Front

    coin: int

    last_get_coin: datetime

    factory_T1: int
    factory_T2: int
    factory_T3: int
    factory_T4: int

    missile_T1: int
    missile_T2: int
    missile_T3: int
    missile_T4: int
    queue: list[Queue_IO]

class UsersIO(SQLModel):
    id: int
    username: str
    front: Front

    coin: int

    last_get_coin: datetime

    factory_T1: int
    factory_T2: int
    factory_T3: int
    factory_T4: int

    missile_T1: int
    missile_T2: int
    missile_T3: int
    missile_T4: int
class UsersList(SQLModel):
    user_list: list[UsersIO]