from fastapi import APIRouter, Response, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.deps import get_session
from app.schemas.auth import UserI, UserLoginI, UserO
from app.services.auth_service import register_user, login_user
from app.api.deps import *
from app.services.info import *
from app.schemas.info import *

router = APIRouter(tags=["factory"])

@router.get("/info", response_model=UserIO)
async def info(user: UserO = Depends(get_user), db: AsyncSession = Depends(get_session)):

    user = get_info(user.id, db)
    return user

@router.get("/leadears", response_model=UsersList)
async def info(db: AsyncSession = Depends(get_session)):

    users = get_leadear(db)
    return users