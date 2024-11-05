from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from src.handlers.router import router
from src.keyboards.main import main_menu
from src.states.demolition import Demolition
from src.states.profile import Profile
from src.templates.env import render
from src.templates.keyboard_buttons.call import CALL_MAIN_MENU
from src.templates.keyboard_buttons.demolition import CANCEL_DEMOLITION_CALLBACK
from src.templates.keyboard_buttons.return_back import RETURN_BACK_CALLBACK


@router.message(F.text == CALL_MAIN_MENU)
async def menu_message(message: Message, state: FSMContext) -> None:
    await state.set_state(default_state)
    menu = await message.answer(
        text=render('main.jinja2'),
        reply_markup=main_menu,
    )
    await state.update_data(bot_message_id=menu.message_id)


@router.callback_query(Demolition.waiting_link, F.data == CANCEL_DEMOLITION_CALLBACK)
@router.callback_query(Profile.showing_profile, F.data == RETURN_BACK_CALLBACK)
async def menu_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(default_state)
    await query.message.edit_text(
        text=render('main.jinja2'),
        reply_markup=main_menu,
    )
