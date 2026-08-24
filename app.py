
from datetime import timedelta, datetime, timezone
import jwt
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select
import os
from dotenv import load_dotenv
from enum import Enum
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

app = FastAPI()

dbName = "db.db"

DbUrl = f"sqlite:///{dbName}"

engine = create_engine(DbUrl)

SQLModel.metadata.create_all(engine)

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

@app.post("/api/v1/register", response_model=UserO)
async def reg(user: UserI, response: Response):

    with Session(engine) as db:
        q = select(User).where(User.username == user.username)
        r = db.exec(q).first()
        if r:
            raise HTTPException(status_code=400, detail="User already exists")
        user_db = User(username=user.username, password=user.password, front=user.front)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        token = await createToken(UserO(id=user_db.id, username=user_db.username, front=user_db.front))
        response.set_cookie(key="token", value=token, httponly=True)


    return UserO(id=user_db.id, username=user_db.username, front=user_db.front)

@app.post("/api/v1/login", response_model=UserO)
async def login(user: UserI, response: Response):
    with Session(engine) as db:
        q = select(User).where((User.username == user.username) & (User.password == user.password))
        r = db.exec(q).first()
        if not r:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        token = await createToken(UserO(id=r.id, username=r.username, front=r.front))
        response.set_cookie(key="token", value=token, httponly=True)
    return UserO(id=r.id, username=r.username, front=r.front)


