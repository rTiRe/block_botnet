from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.enums import ChatMemberStatus
from aiogram.types import CallbackQuery, Message, TelegramObject

from src.keyboards.channel import follow_channel
from src.templates.keyboard_buttons.channel import MAIN_CHANNEL_ID


class CheckSubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        function_handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        event_data: Dict[str, Any],
    ) -> Any:
        user = event_data['event_from_user']
        is_member = (await event.bot.get_chat_member(MAIN_CHANNEL_ID, user.id)).status not in {
            ChatMemberStatus.KICKED,
            ChatMemberStatus.LEFT,
            ChatMemberStatus.RESTRICTED,
        }
        if is_member:
            return await function_handler(event, event_data)
        if isinstance(event, CallbackQuery):
            await event.answer()
        if isinstance(event, Message):
            await event.delete()
        await event.bot.send_message(
            user.id,
            text='Для работы бота необходима подписка на канал!',
            reply_markup=follow_channel,
        )
