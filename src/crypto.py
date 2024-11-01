from aiocryptopay import AioCryptoPay

crypto: AioCryptoPay


def setup_crypto(_crypto: AioCryptoPay) -> None:
    global crypto
    crypto = _crypto


def get_crypto() -> AioCryptoPay:
    global crypto
    return crypto
