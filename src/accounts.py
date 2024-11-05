from pyrogram import Client, errors
import asyncio
from config.settings import settings
from os import listdir

accounts: list[Client]


async def _setup_account(session_name: str) -> None | Client:
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
        return
    if not is_authorized:
        return
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
        return
    return app

async def setup_accounts() -> None:
    global accounts
    accounts = []
    files = listdir(settings.SESSIONS_PATH)
    sessions = [file_name[:-8] for file_name in files if file_name.endswith('.session')]
    pre_setup_accounts = await asyncio.gather(*[_setup_account(session) for session in sessions])
    accounts = list(filter(lambda account: account is not None, pre_setup_accounts))


def get_accounts() -> list[Client]:
    global accounts
    return accounts


async def disconnect_accounts() -> None:
    for account in accounts:
        await account.disconnect()
