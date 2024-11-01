from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.admin import Admin
from src.storage.database import get_db
from src.utils.inject_database import Provide, inject


@inject
async def check_admin(user_id: int, session: AsyncSession = Provide(get_db)) -> bool:
    statement = select(Admin).where(Admin.user_id == user_id)
    raw_admin = await session.execute(statement)
    return bool(raw_admin.fetchone())


@inject
async def add_admin(user_id: int, session: AsyncSession = Provide(get_db)) -> None:
    statement = insert(Admin).values(user_id=user_id)
    await session.execute(statement)
    await session.commit()
