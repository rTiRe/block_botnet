from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.crypto import get_crypto
from src.handlers.subscription.router import router
from src.keyboards.pay import pay_keyboard
from src.states.subscription import Subscription
from src.templates.env import render
from src.templates.keyboard_buttons.subscription import SUBSCRIPTIONS
from src.utils.crypto_utils import add_user_invoice_id, get_user_invoice_id


@router.callback_query(Subscription.selecting_subscription, F.data.in_(list(SUBSCRIPTIONS.keys())))
async def pay_subscription(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    invoice_data: dict = SUBSCRIPTIONS[query.data]['invoice'].copy()
    invoice_data['paid_btn_url'] = f'https://t.me/{(await query.bot.get_me()).username}'
    invoice_data['payload'] = f'{query.from_user.id},{SUBSCRIPTIONS[query.data]['duration']}'
    crypto = get_crypto()
    invoice = await crypto.create_invoice(**invoice_data)
    old_invoice = await get_user_invoice_id(query.from_user.id)
    if invoice.invoice_id != old_invoice:
        if old_invoice:
            await crypto.delete_invoice(invoice.invoice_id)
        await add_user_invoice_id(query.from_user.id, invoice.invoice_id)
    await state.set_state(Subscription.paying_subscription)
    await query.message.edit_text(
        text=render('pay.jinja2', invoice=invoice),
        reply_markup=await pay_keyboard(invoice),
    )
