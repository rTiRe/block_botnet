import time

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.utils.user_utils import get_user
from src.utils.admin_utils import check_admin
from src.storage.database import get_db
from src.models.user import User
from src.utils.inject_database import Provide, inject

@inject
async def add_subscription(
    user_id: int,
    subscription_timestamp: int,
    session: AsyncSession = Provide(get_db),
) -> None:
    statement = update(
        User,
    ).where(
        User.user_id == user_id,
    ).values(
        subscription=subscription_timestamp,
    )
    await session.execute(statement)
    await session.commit()


@inject
async def remove_subscription(user_id: int, session: AsyncSession = Provide(get_db)) -> None:
    statement = update(
        User,
    ).where(
        User.user_id == user_id,
    ).values(
        subscription=None,
    )
    await session.execute(statement)
    await session.commit()


async def check_subscription(user_id: int) -> str | bool:
    if await check_admin(user_id):
        return f'∞'
    user = await get_user(user_id)
    if not user or not user.subscription:
        return False
    if user.subscription == -1:
        return f'∞'
    now = datetime.fromtimestamp(time.time())
    subscription_end = datetime.fromtimestamp(user.subscription / 1000)
    delta = subscription_end - now
    if delta.total_seconds() > 0:
        hours = delta.seconds // 3600
        minutes = (delta.seconds // 60) % 60
        seconds = delta.seconds - hours * 3600 - minutes * 60
        return f'{delta.days} д. {hours} ч. {minutes} м. {seconds} с.'
    return False