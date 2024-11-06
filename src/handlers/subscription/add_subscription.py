import time

from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from src.handlers.subscription.router import router
from src.utils.admin_utils import check_admin
from src.utils.subscription_utils import add_subscription as add_sub


@router.message(Command('add'))
async def add_subscription(message: Message, command: CommandObject) -> None:
    await message.delete()
    if not await check_admin(message.from_user.id):
        await message.answer('У вас недостаточно прав, обратитесь к администратору!')
        return
    if len(command.args) < 2:
        await message.answer('Неправильный формат команды. Используйте: /add [target_user_id] [days]')
        return
    command_args = command.args.split(' ')
    try:
        target_user_id, days = map(int, command_args[:2])
    except ValueError:
        await message.answer(
            'ID и количество дней должны быть числами. Используйте: /add [target_user_id] [days]',
        )
        return
    if days == -1:
        subscription_timestamp = -1
    else:
        days_milliseconds = days * 24 * 60 * 60 * 1000
        subscription_timestamp = int(time.time() * 1000) + days_milliseconds
    try:
        await add_sub(target_user_id, subscription_timestamp)
    except Exception:  # noqa: PIE786 - Because the user should not know the reason for the error.
        await message.answer('Произошла ошибка! Возможно, указанного пользователя не существует.')
    else:
        await message.answer(f'Подписка на {days} дней успешно выдана пользователю {target_user_id}!')
