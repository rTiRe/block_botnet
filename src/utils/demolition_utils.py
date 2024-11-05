import time

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.storage.database import get_db
from src.utils.admin_utils import check_admin
from src.utils.inject_database import Provide, inject
from src.utils.user_utils import get_user
from src.utils.errors import UserWithoutSubscription, UserDemolitionFreezed
from src.utils.subscription_utils import check_subscription
from config.settings import settings


async def get_demolition_timestamp(user_id: int) -> int:
    user = await get_user(user_id)
    return user.demolition_timestamp


async def is_user_can_start_demolition(
    user_id: int,
) -> bool:
    if await check_admin(user_id):
        return True
    if not await check_subscription(user_id):
        raise UserWithoutSubscription()
    timestamp = await get_demolition_timestamp(user_id)
    if timestamp and timestamp >= int(time.time() * 1000):
        wait_time = (timestamp-int(time.time() * 1000)) // 1000
        raise UserDemolitionFreezed(wait_time=wait_time)
    return True


@inject
async def update_demolition_timestamp(
    user_id: int,
    timestamp: int | None = None,
    session: AsyncSession = Provide(get_db),
) -> int:
    if not timestamp:
        timestamp = int(time.time() + settings.DEMOLITION_FREEZE_SECONDS) * 1000
    statement = (
        update(
            User,
        )
        .where(
            User.user_id == user_id,
        )
        .values(
            demolition_timestamp=timestamp,
        )
    )
    await session.execute(statement)
    await session.commit()
    return timestamp
