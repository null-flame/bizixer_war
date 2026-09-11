
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent


TEMPLATE_PATH = BASE_DIR / "templates" / "fastapi_front.html"


@router.get("/")
async def read_root():
    return FileResponse(TEMPLATE_PATH)
