from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.templates.keyboard_buttons.channel import (
    MAIN_CHANNEL,
    MAIN_CHANNEL_URL,
    RULES_CHANNEL,
    RULES_CHANNEL_URL,
)
from src.templates.keyboard_buttons.main import (
    PROFILE,
    PROFILE_CALLBACK,
    START_DEMOLITION,
    START_DEMOLITION_CALLBACK,
    SUPPORT,
    SUPPORT_URL,
)

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=START_DEMOLITION,
                callback_data=START_DEMOLITION_CALLBACK,
            ),
        ],
        [
            InlineKeyboardButton(
                text=PROFILE,
                callback_data=PROFILE_CALLBACK,
            ),
            InlineKeyboardButton(
                text=SUPPORT,
                url=SUPPORT_URL,
            ),
        ],
        [
            InlineKeyboardButton(
                text=RULES_CHANNEL,
                url=RULES_CHANNEL_URL,
            ),
            InlineKeyboardButton(
                text=MAIN_CHANNEL,
                url=MAIN_CHANNEL_URL,
            ),
        ],
    ],
)
