from aiocryptopay.api import Invoice
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.templates.keyboard_buttons.return_back import RETURN_BACK, RETURN_BACK_CALLBACK


async def pay_keyboard(invoice: Invoice) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=RETURN_BACK, callback_data=RETURN_BACK_CALLBACK)
    currency = invoice.asset or invoice.fiat
    builder.button(text=f'{invoice.amount} {currency}', url=invoice.bot_invoice_url)
    builder.adjust(1, repeat=True)
    return builder.as_markup()
