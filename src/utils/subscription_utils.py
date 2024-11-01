import time
from datetime import datetime

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.storage.database import get_db
from src.utils.admin_utils import check_admin
from src.utils.crypto_utils import check_user_invoice, remove_user_invoice_id
from src.utils.inject_database import Provide, inject
from src.utils.user_utils import get_user

HOUR_SECONDS = 3600


@inject
async def add_subscription(
    user_id: int,
    subscription_timestamp: int | None,
    session: AsyncSession = Provide(get_db),
) -> None:
    statement = (
        update(
            User,
        )
        .where(
            User.user_id == user_id,
        )
        .values(
            subscription=subscription_timestamp,
        )
    )
    await session.execute(statement)
    await session.commit()


async def remove_subscription(user_id: int) -> None:
    await add_subscription(user_id, None)


async def check_subscription(user_id: int) -> str | bool:
    if await check_admin(user_id):
        return '∞'
    subscription_timestamp = await check_user_invoice(user_id)
    if subscription_timestamp:
        await add_subscription(user_id, subscription_timestamp)
        await remove_user_invoice_id(user_id)
    user = await get_user(user_id)
    if not user or not user.subscription:
        return False
    if user.subscription == -1:
        return '∞'
    subscription_end = datetime.fromtimestamp(user.subscription / 1000)
    delta = subscription_end - datetime.fromtimestamp(time.time())
    if delta.total_seconds() > 0:
        hours = delta.seconds // HOUR_SECONDS
        minutes = (delta.seconds // 60) % 60
        seconds = delta.seconds - hours * HOUR_SECONDS - minutes * 60
        days = delta.days
        return f'{days} д. {hours} ч. {minutes} м. {seconds} с.'
    return False
