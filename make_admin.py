import asyncio
import sys

import asyncpg
from uuid import uuid4

from config.settings import settings

user_id = int(sys.stdin.readline())


async def make_admin(user_id: int) -> None:
    connection = await asyncpg.connect(
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
    )
    try:
        await connection.execute(f'insert into admins (id, user_id) values (\'{uuid4()}\', {user_id});')
    finally:
        await connection.close()


asyncio.run(make_admin(user_id))