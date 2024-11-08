import asyncio
import random

from pyrogram import Client, utils, errors
from pyrogram.raw.functions.messages import Report
from pyrogram.raw.types import InputReportReasonSpam

from src.accounts import get_accounts

with open('report_texts.txt') as file:
    REPORT_TEXTS = tuple([line.strip() for line in file.readlines()])


def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith('-'):
        return 'user'
    elif peer_id_str.startswith('-100'):
        return 'channel'
    else:
        return 'chat'


utils.get_peer_type = get_peer_type_new


async def report(app: Client, chat_id: str | int, message_id: int) -> bool:
    try:
        chat = await app.resolve_peer(peer_id=chat_id)
    except Exception:
        return False
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
    except errors.RPCError as exception:
        print(exception)
        return False
    except Exception:  # noqa: PIE786 - Because we catch all Exceptions
        return False
    return True


async def demolition(chat_id: int, message_id: int) -> tuple[int, int]:
    async with asyncio.TaskGroup() as taskgroup:
        reports_tasks = [
            taskgroup.create_task(report(account, chat_id, message_id)) for account in get_accounts().values()
        ]
    reports_result = [task.result() for task in reports_tasks]
    return reports_result.count(True), reports_result.count(False)
