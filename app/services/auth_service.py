from fastapi import HTTPException, Response
from sqlmodel import select

from app.core.database import engine, AsyncSession
from app.core.security import createToken
from app.models.user import User
from app.schemas.auth import UserI, UserLoginI, UserO


async def register_user(user: UserI, response: Response, db: AsyncSession):
    
    q = select(User).where(User.username == user.username)
    r = await db.exec(q)
    r = r.first()
    if r:
        raise HTTPException(status_code=400, detail="User already exists")
    user_db = User(username=user.username, password=user.password, front=user.front)
    db.add(user_db)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error occurred while registering user")
    await db.refresh(user_db)
    token = await createToken(UserO(id=user_db.id, username=user_db.username, front=user_db.front))
    response.set_cookie(key="token", value=token, httponly=True)
    return UserO(id=user_db.id, username=user_db.username, front=user_db.front)


async def login_user(user: UserLoginI, response: Response, db: AsyncSession):

    q = select(User).where((User.username == user.username) & (User.password == user.password))
    r = await db.exec(q)
    r: User = r.first()
    if not r:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = await createToken(UserO(id=r.id, username=r.username, front=r.front))
    response.set_cookie(key="token", value=token, httponly=True)
    return UserO(id=r.id, username=r.username, front=r.front)
