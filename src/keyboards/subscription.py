from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.templates.keyboard_buttons.subscription import ONE_WEEK, ONE_WEEK_CALLBACK

subscription_select_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=ONE_WEEK, callback_data=ONE_WEEK_CALLBACK)],
    ]
)
