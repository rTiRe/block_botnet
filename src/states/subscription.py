from aiogram.fsm.state import State, StatesGroup

class Subscription(StatesGroup):
    selecting_subscription = State()
