import time

from aiocryptopay.const import InvoiceStatus
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.crypto import get_crypto
from src.models.user import User
from src.storage.database import get_db
from src.utils.admin_utils import check_admin
from src.utils.inject_database import Provide, inject
from src.utils.user_utils import get_user


async def get_user_invoice_id(user_id: int) -> int:
    if await check_admin(user_id):
        return None
    user = await get_user(user_id)
    return user.waiting_invoice


@inject
async def add_user_invoice_id(
    user_id: int,
    invoice_id: int | None,
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
            waiting_invoice=invoice_id,
        )
    )
    await session.execute(statement)
    await session.commit()


async def remove_user_invoice_id(user_id: int) -> None:
    await add_user_invoice_id(user_id, None)


async def check_user_invoice(user_id: int) -> int | bool:
    invoice_id = await get_user_invoice_id(user_id)
    if invoice_id:
        crypto = get_crypto()
        invoice = await crypto.get_invoices(invoice_ids=invoice_id)
        if invoice.status == InvoiceStatus.PAID:
            days = int(invoice.payload.split(',')[1].strip())
            if days == -1:
                subscription_timestamp = -1
            else:
                days_milliseconds = days * 24 * 60 * 60 * 1000
                subscription_timestamp = int(time.time() * 1000) + days_milliseconds
            return subscription_timestamp
    return False
