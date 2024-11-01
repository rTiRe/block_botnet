from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.templates.keyboard_buttons.channel import (MAIN_CHANNEL,
                                                    MAIN_CHANNEL_URL)

follow_channel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=MAIN_CHANNEL, url=MAIN_CHANNEL_URL)],
    ]
)
