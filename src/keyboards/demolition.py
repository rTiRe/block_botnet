from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.templates.keyboard_buttons.demolition import CANCEL_DEMOLITION, CANCEL_DEMOLITION_CALLBACK

cancel_demolition = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=CANCEL_DEMOLITION, callback_data=CANCEL_DEMOLITION_CALLBACK)],
    ],
)
