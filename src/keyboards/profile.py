from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.templates.keyboard_buttons.channel import MAIN_CHANNEL, MAIN_CHANNEL_URL
from src.templates.keyboard_buttons.profile import BUY_SUBSCRIPTION, BUY_SUBSCRIPTION_CALLBACK


async def profile_keyboard(subscription: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=MAIN_CHANNEL, url=MAIN_CHANNEL_URL)
    if not subscription:
        builder.button(text=BUY_SUBSCRIPTION, callback_data=BUY_SUBSCRIPTION_CALLBACK)
    builder.adjust(1, 1)
    return builder.as_markup()
