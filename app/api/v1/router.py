from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.coin import router as coin_router
from app.api.v1.factory import router as factory_router
from app.api.v1.missile import router as missile_router
from app.api.v1.info import router as info_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(coin_router)
router.include_router(factory_router)
router.include_router(missile_router)
router.include_router(info_router)
