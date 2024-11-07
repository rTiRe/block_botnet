from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.handlers.main_menu import menu_message
from src.handlers.router import router
from src.keyboards.call import call_main_menu
from src.templates.env import render
from src.templates.keyboard_buttons.channel import CHECK_SUBSCRIPTION_QUERY
from src.utils.user_utils import add_user


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        text=render('start.jinja2'),
        reply_markup=call_main_menu,
    )
    await add_user(message.from_user.id)
    await menu_message(message, state)


@router.callback_query(F.data == CHECK_SUBSCRIPTION_QUERY)
async def check_channel(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    await state.clear()
    await query.message.answer(
        text=render('start.jinja2'),
        reply_markup=call_main_menu,
    )
    await add_user(query.from_user.id)
    await menu_message(query.message, state)
    await query.message.delete()
