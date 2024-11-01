from aiogram.fsm.state import State, StatesGroup


class Demolition(StatesGroup):
    waiting_link = State()
