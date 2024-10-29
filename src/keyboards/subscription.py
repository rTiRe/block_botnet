from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.templates.keyboard_buttons.subscription import ONE_WEEK, ONE_WEEK_CALLBACK
from src.templates.keyboard_buttons.return_back import RETURN_BACK, RETURN_BACK_CALLBACK

subscription_select_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=RETURN_BACK, callback_data=RETURN_BACK_CALLBACK)],
        [InlineKeyboardButton(text=ONE_WEEK, callback_data=ONE_WEEK_CALLBACK)],
    ]
)
