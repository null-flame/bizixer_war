from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_session, get_user
from app.schemas.auth import UserO, BuyFactoryI, BuyFactoryO
from app.services.coin_service import get_coin
from app.services.factory_service import buyFactory
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(tags=["factory"])


@router.post("/buy_factory", response_model=BuyFactoryO)
async def buy_factory_endpoint(factory: BuyFactoryI, user: UserO = Depends(get_user)):
    if factory.count <= 0:
        raise HTTPException(
            status_code=400,
            detail="میزان خرید نمیتواند صفر یا کمتر از صفر باشد!"
        )
    await get_coin(user.id)
    coin = await buyFactory(user.id, factory.count, factory.factory_type)
    return BuyFactoryO(message="Factory bought successfully", coin=coin)
