from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.templates.keyboard_buttons.return_back import RETURN_BACK, RETURN_BACK_CALLBACK
from src.templates.keyboard_buttons.subscription import SUBSCRIPTIONS

subscription_select_builder = InlineKeyboardBuilder()
subscription_select_builder.button(text=RETURN_BACK, callback_data=RETURN_BACK_CALLBACK)
for callback, button_data in SUBSCRIPTIONS.items():
    subscription_select_builder.button(text=button_data['name'], callback_data=callback)
subscription_select_builder.adjust(1, repeat=True)
subscription_select_keyboard = subscription_select_builder.as_markup()
