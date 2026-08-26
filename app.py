from contextlib import asynccontextmanager
from datetime import timedelta, datetime, timezone
import os
import jwt
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio import AsyncSession, create_async_engine
from enum import Enum
from dotenv import load_dotenv

load_dotenv()


class Front(str, Enum):
    mahdi = "mahdi"
    fere = "fere"
    gooji = "gooji"

class User(SQLModel, table=True):
    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    front: Front

class UserI(SQLModel):
    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)
    username: str
    password: str
    front: Front

class UserO(SQLModel):
    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)
    id: int
    username: str
    front: Front

app = FastAPI(lifespan=on_startup)

dbName = "db.db"

DbUrl = f"sqlite+aiosqlite:///{dbName}"

engine = create_async_engine(DbUrl)

ALG = "HS256"


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



async def get_user(request: Request):
    token = request.cookies.get("token")
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
@asynccontextmanager
async def on_startup(app: FastAPI):
    async with engine.begin() as db:
        await db.run_sync(SQLModel.metadata.create_all)

    yield

    await engine.dispose()

@app.post("/api/v1/register", response_model=UserO)
async def reg(user: UserI, response: Response):

    async with AsyncSession(engine) as db:
        q = select(User).where(User.username == user.username)
        r = await db.execute(q)
        r = r.first()
        if r:
            raise HTTPException(status_code=400, detail="User already exists")
        user_db = User(username=user.username, password=user.password, front=user.front)
        db.add(user_db)
        await db.commit()
        await db.refresh(user_db)
        token = await createToken(UserO(id=user_db.id, username=user_db.username, front=user_db.front))
        response.set_cookie(key="token", value=token, httponly=True)


    return UserO(id=user_db.id, username=user_db.username, front=user_db.front)

@app.post("/api/v1/login", response_model=UserO)
async def login(user: UserI, response: Response):
    async with AsyncSession(engine) as db:
        q = select(User).where((User.username == user.username) & (User.password == user.password))
        r = await db.execute(q)
        r = r.first()
        if not r:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        token = await createToken(UserO(id=r.id, username=r.username, front=r.front))
        response.set_cookie(key="token", value=token, httponly=True)
    return UserO(id=r.id, username=r.username, front=r.front)


