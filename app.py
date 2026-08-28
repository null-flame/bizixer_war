from contextlib import asynccontextmanager
from datetime import timedelta, datetime, timezone
import os
import jwt
from fastapi import FastAPI, HTTPException, Request, Response, Depends, Cookie
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel, select, Relationship
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from enum import Enum
from dotenv import load_dotenv

T1_factory = 12
T2_factory = 125
T3_factory = 625
T4_factory = 2083



class TType(str, Enum):
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"
    T4 = "T4"

factory_costs = {
        TType.T1: 30,
        TType.T2: 500,
        TType.T3: 10000,
        TType.T4: 100000,
    }
missile_costs = {
        TType.T1: 60,
        TType.T2: 625,
        TType.T3: 625*6,
        TType.T4: 2083*6,
    }
factory_health = {
        TType.T1: 90,
        TType.T2: 1500,
        TType.T3: 15000,
        TType.T4: 150000,
    }

missile_time = {
        TType.T1: 2,
        TType.T2: 15,
        TType.T3: 60,
        TType.T4: 120,
    }
load_dotenv()

class get_coin_out(SQLModel):
    message: str
    coin: int

class buyfactoryI(SQLModel):
    factory_type: TType
    count: int
class buyfactoryO(SQLModel):
    message: str
    coin: int
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

    coin: int = Field(default=500)

    last_get_coin: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    factory_T1: int = Field(default=100)
    factory_T2: int = Field(default=0)
    factory_T3: int = Field(default=0)
    factory_T4: int = Field(default=0)

    last_attacked_at: datetime | None = Field(default=None)

    missile_T1: int = Field(default=0)
    missile_T2: int = Field(default=0)
    missile_T3: int = Field(default=0)
    missile_T4: int = Field(default=0)


class Queue(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    count: int | None
    model: TType
    create_time: datetime
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    user: Optional[User] = Relationship()  

class UserI(SQLModel):
    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)
    username: str = Field(index=True, unique=True)
    password: str
    front: Front

class UserO(SQLModel):
    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)
    id: int
    username: str
    front: Front


dbName = "db.db"

DbUrl = f"sqlite+aiosqlite:///{dbName}"

engine = create_async_engine(DbUrl)


@asynccontextmanager
async def on_startup(app: FastAPI):
    async with engine.begin() as db:
        await db.run_sync(SQLModel.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(lifespan=on_startup)



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



async def get_user(token: str | None = Cookie(default=None)):
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
    
    


@app.post("/api/v1/register", response_model=UserO)
async def reg(user: UserI, response: Response):

    async with AsyncSession(engine) as db:
        q = select(User).where(User.username == user.username)
        r = await db.exec(q)
        r = r.first()
        if r:
            raise HTTPException(status_code=400, detail="User already exists")
        user_db = User(username=user.username, password=user.password, front=user.front)
        db.add(user_db)
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Error occurred while registering user")
        
        await db.refresh(user_db)
        token = await createToken(UserO(id=user_db.id, username=user_db.username, front=user_db.front))
        response.set_cookie(key="token", value=token, httponly=True)


    return UserO(id=user_db.id, username=user_db.username, front=user_db.front)

@app.post("/api/v1/login", response_model=UserO)
async def login(user: UserI, response: Response):
    async with AsyncSession(engine) as db:
        q = select(User).where((User.username == user.username) & (User.password == user.password))
        r = await db.exec(q)
        r = r.first()
        if not r:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        token = await createToken(UserO(id=r.id, username=r.username, front=r.front))
        response.set_cookie(key="token", value=token, httponly=True)
    return UserO(id=r.id, username=r.username, front=r.front)

async def get_coin(id: int) -> int:
    async with AsyncSession(engine) as db:
        q = select(User).where(User.id == id)
        r = await db.exec(q)
        r = r.first()
        if not r:
            raise HTTPException(status_code=404, detail="User not found")

        factory_T1 = r.factory_T1
        factory_T2 = r.factory_T2
        factory_T3 = r.factory_T3
        factory_T4 = r.factory_T4
        time_now = datetime.now(timezone.utc)
        last_get_coin = r.last_get_coin
        if last_get_coin.tzinfo is None:
            last_get_coin = last_get_coin.replace(tzinfo=timezone.utc)

        sleep_time = (time_now - last_get_coin).total_seconds()
        add_coin = int(
            (factory_T1 * (T1_factory / 3600) * sleep_time)
            + (factory_T2 * (T2_factory / 3600) * sleep_time)
            + (factory_T3 * (T3_factory / 3600) * sleep_time)
            + (factory_T4 * (T4_factory / 3600) * sleep_time)
        )
        
        r.coin += add_coin
        r.last_get_coin = time_now.replace(tzinfo=None)
        coin = r.coin
        try:
            await db.commit()
            await db.refresh(r)
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Error occurred while updating coins")

        return int(coin)

@app.post("/api/v1/get_coin", response_model=get_coin_out)
async def get_coin_endpoint(user: UserO = Depends(get_user)):

    coin = await get_coin(user.id)
    return get_coin_out(message="Coins updated successfully", coin=coin)

async def buyFactory(id: int, count: int, factory_type: TType) -> int:
    async with AsyncSession(engine) as db:
        q = select(User).where(User.id == id)
        r = await db.exec(q)
        r = r.first()
        if not r:
            raise HTTPException(status_code=404, detail="User not found")


        factory_map = {
            TType.T1: "factory_T1",
            TType.T2: "factory_T2",
            TType.T3: "factory_T3",
            TType.T4: "factory_T4",
        }
        total_cost = factory_costs[factory_type] * count
        if r.coin < total_cost:
            raise HTTPException(status_code=400, detail="Not enough coins to buy factories")

        r.coin -= total_cost
        current_count = getattr(r, factory_map[factory_type])
        setattr(r, factory_map[factory_type], current_count + count)
        coin = r.coin
        try:
            await db.commit()
            await db.refresh(r)
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Error occurred while buying factories")
        return coin

@app.post("/api/v1/buy_factory", response_model=buyfactoryO)
async def buy_factory(factory: buyfactoryI, user: UserO = Depends(get_user)):
    await get_coin(user.id)
    coin = await buyFactory(user.id, factory.count, factory.factory_type)
    return buyfactoryO(message="Factory bought successfully" ,coin=coin)

async def get_missiles(id: int):
    async with AsyncSession(engine) as db:
        q = select(User).where(User.id == id)
        r = await db.exec(q)
        r: User = r.first()
        if not r:
            raise HTTPException(status_code=404, detail="User not found")
        q = select(Queue).where(Queue.user_id == r.id)
        res = await db.exec(q)
        res: list[Queue] = res.all()
        now = datetime.now(timezone.utc)
        
        for i in res:
            if i.create_time.tzinfo is None:
                i.create_time = i.create_time.replace(tzinfo=timezone.utc)
            if i.create_time < now:
                if i.model == TType.T1:
                    r.factory_T1 += i.count
                if i.model == TType.T2:
                    r.factory_T2 += i.count
                if i.model == TType.T3:
                    r.factory_T3 += i.count
                if i.model == TType.T4:
                    r.factory_T4 += i.count
                db.delete(i)

        await db.commit()

async def get_lasted_create(id: int) -> datetime:
    async with AsyncSession(engine) as db:
        q = select(Queue).where(Queue.user_id == id).order_by(Queue.id.desc())
        r = await db.exec(q)
        r: Queue = r.first()
        if r is None:
            return datetime.now(timezone.utc)
        return r.create_time

async def buyMissile(id: int, count: int, missile_type: TType) -> int:
    await get_missiles(id)
    async with AsyncSession(engine) as db:
        q = select(User).where(User.id == id)
        r = await db.exec(q)
        r = r.first()
        if not r:
            raise HTTPException(status_code=404, detail="User not found")



        total_cost = missile_costs[missile_type] * count
        if r.coin < total_cost:
            raise HTTPException(status_code=400, detail="Not enough coins to buy factories")
        
        r.coin -= total_cost
        create_time = await get_lasted_create(id)
        create_time = create_time + timedelta(minutes=missile_time[missile_type])
        queue = Queue(count=count, model=missile_type, create_time=create_time, user=r)
        

        coin = r.coin
        db.add(queue)
        try:
            await db.commit()
            await db.refresh(r)
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Error occurred while buying factories")
        return coin

async def attack(id: int, Tid: int, model_missiles: TType, model_factory: TType):

    pass
