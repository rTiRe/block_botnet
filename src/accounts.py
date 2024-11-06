import asyncio
from os import listdir

from pyrogram import Client, errors

from config.settings import settings

accounts: list[Client] = {}


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
    return session_name, app

async def setup_accounts() -> None:
    global accounts
    files = listdir(settings.SESSIONS_PATH)
    sessions = [file_name[:-8] for file_name in files if file_name.endswith('.session') if file_name[:-8] not in accounts.keys()]
    pre_setup_accounts = await asyncio.gather(*[_setup_account(session) for session in sessions])
    pre_setup_accounts = list(filter(lambda x: x is not None, pre_setup_accounts))
    for session_name, account in pre_setup_accounts:
        if account is not None:
            accounts[session_name] = account


def get_accounts() -> dict[str, Client]:
    global accounts
    return accounts


async def disconnect_accounts() -> None:
    for account in accounts:
        await account.disconnect()
