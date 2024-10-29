from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from src.handlers.router import router
from src.templates.keyboard_buttons.return_back import RETURN_BACK_CALLBACK
from src.templates.keyboard_buttons.main import PROFILE_CALLBACK
from src.keyboards.profile import profile_keyboard
from src.templates.env import render
from src.states.profile import Profile
from src.states.subscription import Subscription
from src.utils.subscribtion_utils import check_subscription


@router.callback_query(default_state, F.data == PROFILE_CALLBACK)
@router.callback_query(Subscription.selecting_subscription, F.data == RETURN_BACK_CALLBACK)
async def profile(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    await state.set_state(Profile.showing_profile)
    user_subscription = await check_subscription(query.from_user.id)
    await query.message.edit_text(
        text=render('profile.jinja2', user=query.from_user, subscription=user_subscription),
        reply_markup=await profile_keyboard(user_subscription),
    )