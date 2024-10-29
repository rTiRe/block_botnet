from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.database import get_db
from src.models.admin import Admin
from src.utils.inject_database import Provide, inject

@inject
async def check_admin(user_id: int, session: AsyncSession = Provide(get_db)) -> bool:
    statement = select(Admin).where(Admin.user_id == user_id)
    result = await session.execute(statement)
    if result.fetchone():
        return True
    return False


@inject
async def add_admin(user_id: int, session: AsyncSession = Provide(get_db)) -> None:
    statement = insert(Admin).values(user_id=user_id)
    await session.execute(statement)
    await session.commit()
