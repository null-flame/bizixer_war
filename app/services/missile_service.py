from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException
from sqlmodel import select

from app.core.config import missile_costs, missile_time, factory_health
from app.core.database import engine, AsyncSession
from app.models.enums import TType
from app.models.queue import Queue
from app.models.user import User


async def get_missiles(id: int, db: AsyncSession):
    
    q = select(User).where(User.id == id)
    r = await db.exec(q)
    r: User = r.first()
    if not r:
        raise HTTPException(status_code=404, detail="User not found")
    q = select(Queue).where(Queue.user_id == r.id)
    res = await db.exec(q)
    res: list[Queue] = res.all()
    now = datetime.now(timezone.utc)
    for i in res:
        if i.create_time.tzinfo is None:
            i.create_time = i.create_time.replace(tzinfo=timezone.utc)
        if i.create_time < now:
            if i.model == TType.T1:
                r.missile_T1 += i.count
            if i.model == TType.T2:
                r.missile_T2 += i.count
            if i.model == TType.T3:
                r.missile_T3 += i.count
            if i.model == TType.T4:
                r.missile_T4 += i.count
            db.delete(i)
    await db.commit()


async def get_lasted_create(id: int, db: AsyncSession) -> datetime:
    q = select(Queue).where(Queue.user_id == id).order_by(Queue.id.desc())
    r = await db.exec(q)
    r: Optional[Queue] = r.first()
    if r is None:
        return datetime.now(timezone.utc)
    return r.create_time


async def buyMissile(id: int, count: int, missile_type: TType, db: AsyncSession):
    await get_missiles(id, db)
    q = select(User).where(User.id == id)
    r = await db.exec(q)
    r: User = r.first()
    if not r:
        raise HTTPException(status_code=404, detail="User not found")
    total_cost = missile_costs[missile_type] * count
    if r.coin < total_cost:
        raise HTTPException(status_code=400, detail="Not enough coins to buy factories")
    r.coin -= total_cost
    create_time = await get_lasted_create(id, db)
    create_time = create_time + timedelta(minutes=missile_time[missile_type] * count)
    queue = Queue(count=count, model=missile_type, create_time=create_time, user=r)
    coin = r.coin
    db.add(queue)
    try:
        await db.commit()
        await db.refresh(r)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error occurred while buying factories")
    return coin


async def attack(id: int, Tid: int, model_missiles: TType, model_factory: TType, count: int, db: AsyncSession):
    q = select(User).where(User.id == id)
    r = await db.exec(q)
    r: User = r.first()
    q = select(User).where(User.id == Tid)
    res = await db.exec(q)
    res: User = res.first()
    if res is None:
        raise HTTPException(status_code=404, detail="کاربر وجود ندارد")
    if r is None:
        raise HTTPException(status_code=404, detail="کاربر مهاجم وجود ندارد")
    if r.front == res.front:
        raise HTTPException(status_code=400, detail="شما نمیتوانی هم رزم خود را بزنید!")
    field_name_missle = f"missile_{model_missiles.value}"
    field_name_factory = f"factory_{model_factory.value}"
    missiles_count = getattr(r, field_name_missle)
    factory_count = getattr(res, field_name_factory)
    if missiles_count < count:
        raise HTTPException(status_code=400, detail="شما موشک کافی ندارید!")
    damage = missile_costs[model_missiles] * count
    hp = factory_health[model_factory]
    destroyed = int(damage/hp)
    setattr(r, field_name_missle, missiles_count - count)
    setattr(res, field_name_factory, max(0, factory_count - destroyed))
    await db.commit()
