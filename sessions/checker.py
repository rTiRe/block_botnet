import asyncio
from os import listdir

from pyrogram import Client, errors

API_ID = 'supersecret'
API_HASH = 'supersecret'


async def check_client(session: str) -> None:
    app = Client(session, api_id=API_ID, api_hash=API_HASH)
    is_authorized = await app.connect()
    if not is_authorized:
        print(f'{session} failed')
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
    ):
        print(f'{session} failed')
    else:
        print(f'"{session}" logged in as', me.phone_number)


async def checker() -> tuple[int, int]:
    files = listdir('sessions')
    print(files)
    sessions = [file_name[:-8] for file_name in files if file_name.endswith('.session')]
    await asyncio.gather(*[check_client(session) for session in sessions])

asyncio.run(checker())
