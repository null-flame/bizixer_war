from fastapi import APIRouter, Response, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.deps import get_session
from app.schemas.auth import UserI, UserLoginI, UserO
from app.services.auth_service import register_user, login_user

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserO)
async def register(user: UserI, response: Response, db: AsyncSession = Depends(get_session)):
    return await register_user(user, response, db)


@router.post("/login", response_model=UserO)
async def login(user: UserLoginI, response: Response, db: AsyncSession = Depends(get_session)):
    return await login_user(user, response, db)
