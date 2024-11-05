from aiocryptopay.api import Invoice
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

from aiocryptopay.exceptions.factory import CodeErrorFactory


async def update_user_invoice(user_id: int, invoice_data: dict) -> Invoice:
    crypto = get_crypto()
    invoice = await crypto.create_invoice(**invoice_data)
    old_invoice = await get_user_invoice_id(user_id)
    if invoice.invoice_id != old_invoice:
        if old_invoice:
            try:
                await crypto.delete_invoice(old_invoice)
            except CodeErrorFactory:
                ...
        await add_user_invoice_id(user_id, invoice.invoice_id)
    return invoice


@router.callback_query(Subscription.selecting_subscription, F.data.in_(list(SUBSCRIPTIONS.keys())))
async def pay_subscription(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    invoice_data: dict = SUBSCRIPTIONS[query.data]['invoice'].copy()
    bot_username = (await query.bot.get_me()).username
    invoice_data['paid_btn_url'] = f'https://t.me/{bot_username}'
    user_id = query.from_user.id
    subscription_duration = SUBSCRIPTIONS[query.data]['duration']
    invoice_data['payload'] = f'{user_id},{subscription_duration}'
    invoice = await update_user_invoice(user_id, invoice_data)
    await state.set_state(Subscription.paying_subscription)
    await query.message.edit_text(
        text=render('pay.jinja2', invoice=invoice),
        reply_markup=await pay_keyboard(invoice),
    )
