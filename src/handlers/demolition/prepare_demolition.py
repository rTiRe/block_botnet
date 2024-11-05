from aiogram import F
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.handlers.demolition.router import router
from src.handlers.demolition.run_demolition import demolition
from src.keyboards.demolition import cancel_demolition
from src.states.demolition import Demolition
from src.templates.env import render
from src.templates.keyboard_buttons.main import START_DEMOLITION_CALLBACK
from src.utils.check_link import check_public_link


@router.callback_query(F.data == START_DEMOLITION_CALLBACK)
async def prepare_demolition(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    await state.set_state(Demolition.waiting_link)
    await query.message.edit_text(
        text=render('prepare_demolition.jinja2'),
        reply_markup=cancel_demolition,
    )


@router.message(Demolition.waiting_link)
async def wait_message_link(message: Message, state: FSMContext) -> None:
    link = message.text
    bot_message_id = (await state.get_data()).get('bot_message_id')
    check_result, link_groups = await check_public_link(link)
    if not check_result:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=int(bot_message_id),
            text=render('incorrect_link.jinja2', link=link),
            reply_markup=cancel_demolition,
        )
        await message.delete()
        return
    chat_username = f'@{link_groups[0]}'
    chat = await message.bot.get_chat(chat_username)
    if chat.type != ChatType.SUPERGROUP:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=int(bot_message_id),
            text=render('incorrect_link.jinja2', link=link),
            reply_markup=cancel_demolition,
        )
        await message.delete()
        return
    await message.delete()
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=int(bot_message_id),
        text=render('success_link.jinja2', link=link),
        disable_web_page_preview=True,
    )
    success_reports, failed_reports = await demolition(chat.username, int(link_groups[1]))
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=int(bot_message_id),
        text=render(
            'demolition_end.jinja2',
            link=link,
            success=success_reports,
            fail=failed_reports,
        ),
        reply_markup=cancel_demolition,
        disable_web_page_preview=True,
    )
