from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_session, get_user
from app.models.enums import TType
from app.schemas.auth import UserO
from app.services.coin_service import get_coin
from app.services.missile_service import buyMissile, attack
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.missile import *
router = APIRouter(tags=["missile"])


@router.post("/buy_missile", response_model=buy_missile_out)
async def buy_missile_endpoint(
    data: buy_missile_In,
    user: UserO = Depends(get_user),
    db: AsyncSession = Depends(get_session)
):
    if data.count <= 0:
        raise HTTPException(
            status_code=400,
            detail="میزان خرید نمیتواند صفر یا کمتر از صفر باشد!"
        )
    await get_coin(user.id)
    coin = await buyMissile(user.id, data.count, data.missile_type, db)
    return buy_missile_out(message="Missile purchase initiated", coin=coin)


@router.post("/attack", response_model=attack_out)
async def attack_endpoint(
    data: attack_In,
    user: UserO = Depends(get_user),
    db: AsyncSession = Depends(get_session)
):
    if data.count <= 0:
        raise HTTPException(
            status_code=400,
            detail="میزان حمله نمیتواند صفر یا کمتر از صفر باشد!"
        )
    await attack(user.id, data.Tid, data.missile_type, data.factory_type, data.count, db)
    return attack_out(message="Attack successful")

@router.post("/get_missiles", response_model=attack_out)
async def get__missiles_api(user: UserO = Depends(get_user), db: AsyncSession = Depends(get_session)):
    await get_session(user.id, db)
    return attack_out(meesage="موشک های شما با موفقیت جمع اوری شدند")
