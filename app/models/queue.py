from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.enums import TType

if TYPE_CHECKING:
    from app.models.user import User


class Queue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    count: Optional[int]
    model: TType
    create_time: datetime
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="queues")
