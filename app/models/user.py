from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel

from app.models.enums import Front

if TYPE_CHECKING:
    from app.models.queue import Queue


class User(SQLModel, table=True):
    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    front: Front

    coin: int = Field(default=500)

    last_get_coin: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    factory_T1: int = Field(default=100)
    factory_T2: int = Field(default=0)
    factory_T3: int = Field(default=0)
    factory_T4: int = Field(default=0)

    last_attacked_at: Optional[datetime] = Field(default=None)

    missile_T1: int = Field(default=0)
    missile_T2: int = Field(default=0)
    missile_T3: int = Field(default=0)
    missile_T4: int = Field(default=0)

    queues: list["Queue"] = Relationship(back_populates="user")
