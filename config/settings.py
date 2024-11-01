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

    WEBHOOK_URL: Optional[str]

    @property
    def db_url(self) -> str:
        protocol = 'postgresql+asyncpg'
        user_data = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        server_data = f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}'
        return f'{protocol}://{user_data}@{server_data}/{self.POSTGRES_DB}'

    @property
    def bot_webhook_url(self) -> str:
        return f'{self.WEBHOOK_URL}/{self.BOT_WEBHOOK_PATH}'

    @property
    def crypro_webhook_url(self) -> str:
        return f'{self.WEBHOOK_URL}/{self.CRYPTO_WEBHOOK_PATH}'

    class Config:
        env_file = 'config/.env'


settings = Settings()
