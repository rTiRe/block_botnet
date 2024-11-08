import asyncio
from os import listdir

from pyrogram import Client, errors

API_ID = 'supersecret'
API_HASH = 'supersecret'

success_logged = []


async def check_client(session: str) -> None:
    app = Client(session, api_id=API_ID, api_hash=API_HASH)
    try:
        async with asyncio.timeout(60):
            is_authorized = await app.connect()
    except asyncio.TimeoutError:
        print(f'{session} - timed out')
        return
    except Exception as exception:
        print(f'{session} failed: {exception}', flush=True)
    if not is_authorized:
        print(f'{session} failed: not authorized.')
    try:
        me = await app.get_me()
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
        print(f'{session} failed: {exception}.')
    else:
        success_logged.append(session)
        print(f'"{session}" logged in as', me.phone_number)


async def checker() -> tuple[int, int]:
    files = listdir('sessions')
    print(f'All sessions: {files}')
    sessions = [file_name[:-8] for file_name in files if file_name.endswith('.session')]
    async with asyncio.TaskGroup() as taskgroup:
        for session in sessions:
            taskgroup.create_task(check_client(session))
    print()
    print(f'{len(success_logged)}/{len(sessions)} working_setup_account sessions.')
    for session in success_logged:
        print(session)

asyncio.run(checker())
