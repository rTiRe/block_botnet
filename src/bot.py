from aiogram import Bot, Dispatcher

bot: Bot
dp: Dispatcher


def setup_bot(_bot: Bot) -> None:
    global bot
    bot = _bot


def get_bot() -> Bot:
    global bot
    return bot


def setup_dp(_dp: Dispatcher) -> None:
    global dp
    dp = _dp


def get_dp() -> Dispatcher:
    global dp
    return dp
