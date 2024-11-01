from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.handlers.subscription.router import router
from src.templates.keyboard_buttons.profile import BUY_SUBSCRIPTION_CALLBACK
from src.templates.env import render
from src.keyboards.subscription import subscription_select_keyboard
from src.states.profile import Profile
from src.states.subscription import Subscription
from src.utils.subscription_utils import check_subscription

@router.callback_query(Profile.showing_profile, F.data == BUY_SUBSCRIPTION_CALLBACK)
async def select_subscription(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    if await check_subscription(query.from_user.id):
        return
    await state.set_state(Subscription.selecting_subscription)
    await query.message.edit_text(
        text=render('select_subscription.jinja2'),
        reply_markup=subscription_select_keyboard,
    )
