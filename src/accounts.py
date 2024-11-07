import asyncio
from os import listdir

from pyrogram import Client, errors

from config.settings import settings

accounts: dict[str, Client] = {}


async def _setup_account(session_name: str) -> None | Client:
    app = Client(
        f'./../{settings.SESSIONS_PATH}{session_name}',
        api_id=settings.API_ID,
        api_hash=settings.API_HASH,
        proxy=settings.proxy,
    )
    try:
        async with asyncio.timeout(20):
            is_authorized = await app.connect()
    except asyncio.TimeoutError:
        print(f'{session_name} - timed out', flush=True)
        return False
    except Exception as exception:
        print(f'{session_name} - {exception}', flush=True)
        return False
    if not is_authorized:
        print(f'{session_name} - not authorized', flush=True)
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
        errors.FloodWait,
        Exception,
    ) as exception:
        print(f'{session_name} - {exception}', flush=True)
        await app.disconnect()
        return False
    print(f'{session_name} - success', flush=True)
    return session_name, app

async def setup_accounts() -> None:
    global accounts
    files = listdir(settings.SESSIONS_PATH)
    sessions = [file_name[:-8] for file_name in files if file_name.endswith('.session') if file_name[:-8] not in accounts.keys()]
    print(f'Tries to setup accounts:', flush=True)
    async with asyncio.TaskGroup() as taskgroup:
        pre_setup_accounts = [taskgroup.create_task(_setup_account(session)) for session in sessions]
    pre_setup_accounts = list(filter(lambda x: x.result(), pre_setup_accounts))
    for task in pre_setup_accounts:
        session_name, account = task.result()
        if account is not None:
            accounts[session_name] = account
    print('', flush=True)
    print(f'Successfully setup {len(pre_setup_accounts)} accounts:', flush=True)
    for acc in accounts.keys():
        print(acc, flush=True)
    print('', flush=True)


def get_accounts() -> dict[str, Client]:
    global accounts
    return accounts


async def disconnect_accounts() -> None:
    for account in accounts.values():
        await account.disconnect()
