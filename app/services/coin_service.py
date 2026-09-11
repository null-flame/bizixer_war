from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import select

from app.core.config import T1_factory, T2_factory, T3_factory, T4_factory
from app.core.database import engine, AsyncSession
from app.models.user import User


async def get_coin(id: int, db: AsyncSession):

    q = select(User).where(User.id == id)
    r = await db.exec(q)
    r: User = r.first()
    if not r:
        raise HTTPException(status_code=404, detail="User not found")
    
    factory_T1 = r.factory_T1
    factory_T2 = r.factory_T2
    factory_T3 = r.factory_T3
    factory_T4 = r.factory_T4
    time_now = datetime.now(timezone.utc)
    last_get_coin = r.last_get_coin
    if last_get_coin.tzinfo is None:
        last_get_coin = last_get_coin.replace(tzinfo=timezone.utc)

    sleep_time = (time_now - last_get_coin).total_seconds()
    add_coin = int(
        (factory_T1 * (T1_factory / 3600) * sleep_time)
        + (factory_T2 * (T2_factory / 3600) * sleep_time)
        + (factory_T3 * (T3_factory / 3600) * sleep_time)
        + (factory_T4 * (T4_factory / 3600) * sleep_time)
    )
    r.coin += add_coin
    r.last_get_coin = time_now
    coin = r.coin
    try:
        await db.commit()
        await db.refresh(r)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error occurred while updating coins")
    return int(coin)
