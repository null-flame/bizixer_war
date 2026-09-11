import os
from datetime import datetime, timedelta, timezone
import jwt

from fastapi import HTTPException, Depends
from fastapi.security import APIKeyCookie
from app.core.config import ALG
from app.schemas.auth import UserO

cookie_scheme = APIKeyCookie(name="token")


async def createToken(user: UserO):
    exp = int((datetime.now(timezone.utc) + timedelta(days=30)).timestamp())

    payload = {
        "id": user.id,
        "username": user.username,
        "front": user.front,
        "exp": exp
    }

    encoded_jwt = jwt.encode(payload, os.getenv("sec"), algorithm=ALG)
    return encoded_jwt


async def get_user(token: str = Depends(cookie_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, os.getenv("sec"), algorithms=[ALG])
        user = UserO(id=payload.get("id"), username=payload.get("username"), front=payload.get("front"))
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
