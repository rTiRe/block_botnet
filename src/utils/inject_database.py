import inspect
from typing import Callable


class Provide:
    def __init__(self, function: Callable):
        self.function = function


def inject(function: Callable):
    signature = inspect.signature(function)

    async def wrapper(*args, **kwargs):
        for parameter in signature.parameters.values():
            if isinstance(parameter.default, Provide):
                async for db in parameter.default.function():
                    kwargs[parameter.name] = db
                    return await function(*args, **kwargs)

    return wrapper
