from aiogram.filters import Command
from aiogram.types import Message

from src.handlers.router import router
from src.utils.admin_utils import check_admin

from src.accounts import setup_accounts


@router.message(Command('update_sessions'))
async def update_sessions(message: Message) -> None:
    if not await check_admin(message.from_user.id):
        return
    bot_message = await message.answer(text='Начинаю подгружать сессии...')
    await message.delete()
    await setup_accounts()
    await bot_message.edit_text(text='Сессии успешно подгружены.')
