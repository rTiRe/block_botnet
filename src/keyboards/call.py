from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.templates.keyboard_buttons.call import CALL_MAIN_MENU

call_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=CALL_MAIN_MENU)],
    ],
    resize_keyboard=True,
)
