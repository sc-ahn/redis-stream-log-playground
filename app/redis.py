from redis.asyncio.client import StrictRedis

from app.settings import env

redis = StrictRedis(
    host=env.redis_host,
    port=6379,
    username=env.redis_username,
    password=env.redis_password,
    decode_responses=True,
)


def get_client():
    return redis
