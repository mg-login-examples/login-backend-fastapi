from redis.asyncio.client import Redis


async def redis_add(redis_session: Redis, name: str, key: str, value: str):
    resp = redis_session.hset(name, key, value)
    if isinstance(resp, int):
        raise Exception(f'Failed to add to redis. Response: {resp}')
    return resp


async def redis_remove(redis_session: Redis, name: str, key: str):
    resp = redis_session.hdel(name, key)
    if isinstance(resp, int):
        raise Exception(f'Failed to add to redis. Response: {resp}')
    return resp


async def redis_get(redis_session: Redis, name: str, key: str):
    resp = redis_session.hget(name, key)
    if isinstance(resp, int):
        raise Exception(f'Failed to add to redis. Response: {resp}')
    return resp
