from fastapi import HTTPException, Response
from sqlmodel import select
from app.schemas.info import *
from app.models.user import User
from app.core.database import engine, AsyncSession
from app.models.queue import Queue



async def get_info(id: int, db: AsyncSession):
    q = select(User).where(User.id == id)
    r = await db.exec(q)
    r: User = r.first()
    user = r
    q = select(Queue).where(Queue.user_id == id)
    r = await db.exec(q)
    r: User = r.all()
    user_data = user.model_dump()
    user_data["queue"] = r

    return UserIO.model_validate(user_data)


async def get_leadear(db: AsyncSession):
    q = select(User)
    r = await db.exec(q)
    r: User = r.all()
    users = UsersList(user_list=r)
    return users