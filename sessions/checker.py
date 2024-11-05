import asyncio
from os import listdir

from pyrogram import Client, errors

API_ID = 'supersecret'
API_HASH = 'supersecret'


async def check() -> tuple[int, int]:
    files = listdir('sessions')
    print(files)
    sessions = [file_name[:-8] for file_name in files if file_name.endswith('.session')]
    for session in sessions:
        app = Client(session, api_id=API_ID, api_hash=API_HASH)
        is_authorized = await app.connect()
        if not is_authorized:
            print(f'{session} failed')
            continue
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
            continue
        else:
            print(f'"{session}" logged in as', me.phone_number)

asyncio.run(check())
