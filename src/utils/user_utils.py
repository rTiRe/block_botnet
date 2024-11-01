from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.storage.database import get_db
from src.utils.inject_database import Provide, inject


@inject
async def get_user(user_id: int, session: AsyncSession = Provide(get_db)) -> User:
    statement = select(User).where(User.user_id == user_id)
    result = await session.execute(statement)
    user = result.fetchone()[0]
    return user


@inject
async def get_users(session: AsyncSession = Provide(get_db)) -> tuple[User]:
    statement = select(User.user_id)
    result = await session.execute(statement)
    users = [id[0] for id in result.fetchall()]
    return users


@inject
async def add_user(user_id: int, session: AsyncSession = Provide(get_db)) -> None:
    statement = insert(User).values(user_id=user_id).on_conflict_do_nothing()
    await session.execute(statement)
    await session.commit()

