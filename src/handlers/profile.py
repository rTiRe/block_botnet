import time

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiocryptopay.const import InvoiceStatus

from src.handlers.router import router
from src.templates.keyboard_buttons.return_back import RETURN_BACK_CALLBACK
from src.templates.keyboard_buttons.main import PROFILE_CALLBACK
from src.keyboards.profile import profile_keyboard
from src.templates.env import render
from src.states.profile import Profile
from src.states.subscription import Subscription
from src.utils.subscription_utils import check_subscription, add_subscription
from src.utils.crypto_utils import get_user_invoice_id, remove_user_invoice_id
from src.crypto import get_crypto


@router.callback_query(default_state, F.data == PROFILE_CALLBACK)
@router.callback_query(Subscription.selecting_subscription, F.data == RETURN_BACK_CALLBACK)
@router.callback_query(Subscription.paying_subscription, F.data == RETURN_BACK_CALLBACK)
async def profile(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    await state.set_state(Profile.showing_profile)
    invoice_id = await get_user_invoice_id(query.from_user.id)
    if invoice_id:
        crypto = get_crypto()
        invoice = await crypto.get_invoices(invoice_ids=invoice_id)
        if invoice.status == InvoiceStatus.PAID:
            days = int(invoice.payload.split(',')[1].strip())
            if days == -1:
                subscription_timestamp = -1
            else:
                subscription_timestamp = int(time.time() * 1000) + days * 24 * 60 * 60 * 1000
            await add_subscription(query.from_user.id, subscription_timestamp)
            await remove_user_invoice_id(query.from_user.id)
    user_subscription = await check_subscription(query.from_user.id)
    await query.message.edit_text(
        text=render('profile.jinja2', user=query.from_user, subscription=user_subscription),
        reply_markup=await profile_keyboard(user_subscription),
    )
