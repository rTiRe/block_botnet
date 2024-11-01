from aiogram.types import Message
from aiogram.filters import CommandObject, Command
from aiogram.fsm.state import default_state

from .router import router
from src.utils.admin_utils import check_admin
from src.utils.subscription_utils import remove_subscription as remove_sub

@router.message(default_state, Command('remove'))
async def remove_subscription(message: Message, command: CommandObject) -> None:
    await message.delete()
    if not await check_admin(message.from_user.id):
        await message.answer('У вас недостаточно прав, обратитесь к администратору!')
    if command.args and int(command.args.split(' ')[0]):
        target_user_id = int(command.args.split(' ')[0])
        try:
            await remove_sub(target_user_id)
        except Exception:
            await message.answer('Произошла ошибка!')
            return
        await message.answer('Подписка успешно аннулирована!')
        return
    await message.answer('Неверные аргументы!')
