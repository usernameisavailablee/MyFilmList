from fastapi import  Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.security import verify_token
from src.database import  get_db
from src.auth.service import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    username: str = payload.get("sub")
    user = await get_user_by_username(db, username)
    if not payload or not username or not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user