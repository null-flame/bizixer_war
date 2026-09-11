from fastapi import APIRouter

from app.api.root import router as root_router
from app.api.v1.router import router as api_router

router = APIRouter()

router.include_router(root_router)
router.include_router(api_router)