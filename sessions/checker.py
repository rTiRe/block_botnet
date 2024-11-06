import asyncio
from os import listdir

from pyrogram import Client, errors

API_ID = 'supersecret'
API_HASH = 'supersecret'

success_logged = []


async def check_client(session: str) -> None:
    app = Client(session, api_id=API_ID, api_hash=API_HASH)
    is_authorized = await app.connect()
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
    ) as exception:
        print(f'{session} failed: {exception}.')
    else:
        success_logged.append(session)
        print(f'"{session}" logged in as', me.phone_number)


async def checker() -> tuple[int, int]:
    files = listdir('sessions')
    print(f'All sessions: {files}')
    sessions = [file_name[:-8] for file_name in files if file_name.endswith('.session')]
    await asyncio.gather(*[check_client(session) for session in sessions])
    print()
    print(f'{len(success_logged)} working sessions.')
    for session in success_logged:
        print(session)

asyncio.run(checker())
