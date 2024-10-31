from aiocryptopay import AioCryptoPay

crypto: AioCryptoPay


def setup_crypto(crypto_: AioCryptoPay) -> None:
    global crypto
    crypto = crypto_


def get_crypto() -> AioCryptoPay:
    global crypto
    return crypto
