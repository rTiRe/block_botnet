from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.handlers.subscription.router import router
from src.templates.keyboard_buttons.subscription import SUBSCRIPTIONS
from src.templates.env import render
from src.states.subscription import Subscription
from src.crypto import get_crypto
from src.keyboards.pay import pay_keyboard

@router.callback_query(Subscription.selecting_subscription, F.data.in_(list(SUBSCRIPTIONS.keys())))
async def pay_subscription(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    invoice_data: dict = SUBSCRIPTIONS[query.data]['invoice'].copy()
    invoice_data['paid_btn_url'] = f'https://t.me/{(await query.bot.get_me()).username}'
    invoice_data['payload'] = query.from_user.id
    invoice = await get_crypto().create_invoice(**invoice_data)
    await state.set_state(Subscription.paying_subscription)
    await query.message.edit_text(
        text=render('pay.jinja2', invoice=invoice),
        reply_markup=await pay_keyboard(invoice),
    )
