from redis.asyncio import Redis, ConnectionPool

from config.settings import settings

redis: Redis


def setup_redis() -> Redis:
    global redis
    pool = ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    _redis = Redis(connection_pool=pool)
    redis = _redis
    return redis


def get_redis() -> Redis:
    global redis
    return redis