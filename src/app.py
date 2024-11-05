import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update
from aiogram import Bot, Dispatcher, enums
from aiogram.client.default import DefaultBotProperties
from fastapi import FastAPI
from starlette_context import middleware, plugins

from config.settings import settings
from src import accounts, api, background_tasks, bot, crypto, handlers, middlewares


# А я хз как работать с вебхуками cryptobot, тут тестить надо
async def invoice_paid(update: Update, app) -> None: ...


async def setup_app() -> tuple[Dispatcher, Bot, AioCryptoPay]:
    dp = Dispatcher()
    bot.setup_dp(dp)
    dp.include_router(handlers.router)
    dp.message.outer_middleware(middlewares.CheckSubscriptionMiddleware())
    dp.callback_query.outer_middleware(middlewares.CheckSubscriptionMiddleware())
    default = DefaultBotProperties(parse_mode=enums.ParseMode.HTML)
    tg_bot = Bot(token=settings.BOT_TOKEN, default=default)
    bot.setup_bot(tg_bot)
    tg_crypto = AioCryptoPay(token=settings.CRYPTO_PAY_TOKEN, network=Networks.TEST_NET)
    crypto.setup_crypto(tg_crypto)
    return dp, tg_bot, tg_crypto


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    _dp, tg_bot, tg_crypto = await setup_app()
    tg_crypto.register_pay_handler(invoice_paid)
    await tg_bot.set_webhook(settings.bot_webhook_url)
    await accounts.setup_accounts()
    yield
    while background_tasks:
        await asyncio.sleep(0)
    await accounts.disconnect_accounts()
    await tg_bot.delete_webhook()
    await tg_crypto.close()


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    app.include_router(api.router)
    app.add_middleware(middleware.RawContextMiddleware, plugins=[plugins.CorrelationIdPlugin()])
    return app


async def start_polling() -> None:
    dp, tg_bot, _tg_crypto = await setup_app()
    await tg_bot.delete_webhook()
    await accounts.setup_accounts()
    await dp.start_polling(tg_bot)


if __name__ == '__main__':
    if settings.FASTAPI_HOST:
        uvicorn.run(
            'src.app:create_app',
            factory=True,
            host='0.0.0.0',
            port=settings.FASTAPI_PORT,
            workers=1,
        )
    else:
        try:
            asyncio.run(start_polling())
        except KeyboardInterrupt:
            asyncio.run(accounts.disconnect_accounts())
        else:
            asyncio.run(accounts.disconnect_accounts())
