from fastapi import FastAPI

from app.api.v1.router import router
from app.core.database import on_startup

app = FastAPI(lifespan=on_startup)

app.include_router(router)
