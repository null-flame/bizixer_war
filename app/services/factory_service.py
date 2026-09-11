from fastapi import HTTPException
from sqlmodel import select

from app.core.config import factory_costs
from app.core.database import engine, AsyncSession
from app.models.enums import TType
from app.models.user import User


async def buyFactory(id: int, count: int, factory_type: TType, db: AsyncSession):
    q = select(User).where(User.id == id)
    r = await db.exec(q)
    r: User = r.first()
    if not r:
        raise HTTPException(status_code=404, detail="User not found")
    factory_map = {
        TType.T1: "factory_T1",
        TType.T2: "factory_T2",
        TType.T3: "factory_T3",
        TType.T4: "factory_T4",
    }
    total_cost = factory_costs[factory_type] * count
    if r.coin < total_cost:
        raise HTTPException(status_code=400, detail="Not enough coins to buy factories")
    r.coin -= total_cost
    current_count = getattr(r, factory_map[factory_type])
    setattr(r, factory_map[factory_type], current_count + count)
    coin = r.coin
    try:
        await db.commit()
        await db.refresh(r)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error occurred while buying factories")
    return coin
