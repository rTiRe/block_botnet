from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.templates.keyboard_buttons.channel import (
    CHECK_SUBSCRIPTION,
    CHECK_SUBSCRIPTION_QUERY,
    MAIN_CHANNEL,
    MAIN_CHANNEL_URL,
)

follow_channel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=MAIN_CHANNEL, url=MAIN_CHANNEL_URL)],
        [InlineKeyboardButton(text=CHECK_SUBSCRIPTION, callback_data=CHECK_SUBSCRIPTION_QUERY)],
    ],
)
