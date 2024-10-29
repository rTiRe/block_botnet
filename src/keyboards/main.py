from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.templates.keyboard_buttons.main import START_DEMOLITION, PROFILE, SUPPORT, START_DEMOLITION_CALLBACK, PROFILE_CALLBACK, SUPPORT_CALLBACK
from src.templates.keyboard_buttons.channel import MAIN_CHANNEL, MAIN_CHANNEL_URL, RULES_CHANNEL, RULES_CHANNEL_URL

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
                callback_data=SUPPORT_CALLBACK,
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
            )
        ],
    ],
)
