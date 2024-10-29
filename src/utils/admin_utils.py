from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.storage.database import get_db
from src.models.admin import Admin

async def check_admin(user_id: int, session: AsyncSession = Depends(get_db)) -> bool:
    statement = select(Admin).where(Admin.user_id == user_id)
    result = await session.execute(statement)
    if result.fetchone():
        return True
    return False


async def add_admin(user_id: int, session: AsyncSession = Depends(get_db)) -> None:
    statement = insert(Admin).values(user_id=user_id)
    await session.execute(statement)
    await session.commit()
