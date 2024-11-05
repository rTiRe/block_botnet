import asyncio
import random
from os import listdir

from pyrogram import Client, errors
from pyrogram.raw.functions.messages import Report
from pyrogram.raw.types import InputReportReasonSpam

from config.settings import settings

REPORT_TEXTS = (
    'Сообщение содержит спам',
    'Это сообщение нарушает правила сообщества',
    'Содержанимое сообщения является неприемлемым',
    'Спам',
    'Спам. Примите меры',
    'Спам. Пожалуйста, примите меры',
    'Этот контент нарушает политику сервиса',
    'Этот контент нарушает политику Телаграмм',
    'Этот контент нарушает политику Telegram',
    'Сообщение кажется подозрительным',
    'Прошу удалить это сообщение',
    'Нарушение правил сообщества. Рассмотрите',
    'Нарушение правил',
)


async def report(app: Client, chat_id: str | int, message_id: int) -> bool:
    chat = await app.resolve_peer(peer_id=chat_id)
    report_message = random.choice(REPORT_TEXTS)
    try:
        await app.invoke(
            Report(
                peer=chat,
                id=[message_id],
                reason=InputReportReasonSpam(),
                message=report_message,
            ),
        )
    except Exception:  # noqa: PIE786 - Because we catch all Exceptions
        return False
    return True


async def prepare_report(session_name: str, chat_id: int, message_id: int) -> bool:
    app = Client(
        f'./../{settings.SESSIONS_PATH}{session_name}',
        api_id=settings.API_ID,
        api_hash=settings.API_HASH,
        proxy=settings.proxy,
    )
    try:
        async with asyncio.timeout(5):
            is_authorized = await app.connect()
    except asyncio.TimeoutError:
        return False
    if not is_authorized:
        return False
    try:
        await app.get_me()
    except (
        errors.ActiveUserRequired,
        errors.AuthKeyInvalid,
        errors.AuthKeyPermEmpty,
        errors.AuthKeyUnregistered,
        errors.AuthKeyDuplicated,
        errors.SessionExpired,
        errors.SessionPasswordNeeded,
        errors.SessionRevoked,
        errors.UserDeactivated,
        errors.UserDeactivatedBan,
    ):
        await app.disconnect()
        return False
    if await report(app, chat_id, message_id):
        await app.disconnect()
        return True
    await app.disconnect()
    return False


async def demolition(chat_id: int, message_id: int) -> tuple[int, int]:
    files = listdir(settings.SESSIONS_PATH)
    sessions = [file_name[:-8] for file_name in files if file_name.endswith('.session')]
    reports_result = await asyncio.gather(
        *[prepare_report(session, chat_id, message_id) for session in sessions],
    )
    return reports_result.count(True), reports_result.count(False)
