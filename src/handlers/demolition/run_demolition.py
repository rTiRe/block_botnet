import asyncio
import random

from pyrogram import Client
from pyrogram.raw.functions.messages import Report
from pyrogram.raw.types import InputReportReasonSpam

from src.accounts import get_accounts

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
    await asyncio.sleep(random.randint(0, 15))
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


async def demolition(chat_id: int, message_id: int) -> tuple[int, int]:
    reports_result = await asyncio.gather(
        *[report(account, chat_id, message_id) for account in get_accounts()],
    )
    return reports_result.count(True), reports_result.count(False)
