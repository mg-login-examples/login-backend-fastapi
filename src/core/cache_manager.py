from core.helper_classes.redisCacheManager import RedisCacheManager

def get_cache_manager(redis_url: str, redis_user: str, redis_password: str) -> RedisCacheManager:
    app_cache_manager = RedisCacheManager(
        redis_url,
        redis_user,
        redis_password
    )
    return app_cache_manager
