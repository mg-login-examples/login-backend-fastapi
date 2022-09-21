from stores.access_tokens_store.access_token_store_manager import AccessTokenStoreManager

def get_access_token_store_manager(
        store_type: str,
        redis_url: str = None,
        redis_user: str = None,
        redis_password: str = None,
        is_admin=False
    ):
    redis_token_prefix = "admin" if is_admin else "user"
    user_api_tokens_file_name: str = "user_access_tokens.txt"
    admin_api_tokens_file_name: str = "admin_access_tokens.txt"
    access_tokens_file_name = admin_api_tokens_file_name if is_admin else user_api_tokens_file_name

    return AccessTokenStoreManager(
        store_type=store_type,
        redis_url=redis_url,
        redis_user=redis_user,
        redis_password=redis_password,
        redis_token_prefix=redis_token_prefix,
        file_name=access_tokens_file_name,
    )
