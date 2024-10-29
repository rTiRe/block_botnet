from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from src.utils.user_utils import add_user

from src.handlers.router import router
from src.keyboards.call import call_main_menu
from src.templates.env import render
from src.handlers.main_menu import menu_message


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.set_state(default_state)
    await message.answer(
        text=render('start.jinja2'),
        reply_markup=call_main_menu,
    )
    await add_user(message.from_user.id)
    await message.delete()
    await menu_message(message, state)