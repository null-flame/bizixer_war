from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.deps import get_session, get_user
from app.schemas.auth import UserO, get_coin_out
from app.services.coin_service import get_coin

router = APIRouter(tags=["coin"])


@router.post("/get_coin", response_model=get_coin_out)
async def get_coin_endpoint(user: UserO = Depends(get_user), db: AsyncSession = Depends(get_session)):
    coin = await get_coin(user.id, db)
    return get_coin_out(message="Coins updated successfully", coin=coin)
