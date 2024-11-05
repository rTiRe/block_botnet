class UserWithoutSubscription(Exception):
    ...


class UserDemolitionFreezed(Exception):
    def __init__(self, wait_time: int) -> None:
        super().__init__(f'wait_time={wait_time}')
