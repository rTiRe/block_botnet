from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_WEBHOOK_PATH: str

    CRYPTO_PAY_TOKEN: str
    CRYPTO_WEBHOOK_PATH: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int

    FASTAPI_HOST: Optional[str]
    FASTAPI_PORT: Optional[int]

    API_ID: str
    API_HASH: str

    SESSIONS_PATH: str

    PROXY_SCHEME: Optional[str]
    PROXY_USERNAME: str
    PROXY_PASSWORD: str
    PROXY_HOSTNAME: str
    PROXY_PORT: int

    DEMOLITION_FREEZE_SECONDS: Optional[int]

    LOGS_CHAT_ID: str
    MAIN_CHANNEL_URL: str
    MAIN_CHANNEL_ID: str
    RULES_CHANNEL_URL: str
    SUPPORT_URL: str

    DEVMODE: Optional[bool]

    @property
    def db_url(self) -> str:
        protocol = 'postgresql+asyncpg'
        user_data = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        server_data = f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}'
        return f'{protocol}://{user_data}@{server_data}/{self.POSTGRES_DB}'

    @property
    def bot_webhook_url(self) -> str:
        return f'{self.FASTAPI_HOST}/{self.BOT_WEBHOOK_PATH}'

    @property
    def crypro_webhook_url(self) -> str:
        return f'{self.FASTAPI_HOST}/{self.CRYPTO_WEBHOOK_PATH}'

    @property
    def proxy(self) -> dict:
        if not self.PROXY_SCHEME:
            return
        return {
            'scheme': self.PROXY_SCHEME,
            'hostname': self.PROXY_HOSTNAME,
            'port': self.PROXY_PORT,
            'username': self.PROXY_USERNAME,
            'password': self.PROXY_PASSWORD,
        }

    class Config:
        env_file = 'config/.env'


settings = Settings()
