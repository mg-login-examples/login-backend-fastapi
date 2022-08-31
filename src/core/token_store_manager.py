from data.access_tokens_store.access_token_store_manager import AccessTokenStoreManager
from core.helper_classes.settings import Settings

def get_api_token_store_manager(SETTINGS: Settings, is_admin=False):
    if is_admin:
        return AccessTokenStoreManager(
            store_type=SETTINGS.session_token_store_type,
            file_name=SETTINGS.admin_api_tokens_file_name,
            redis_url=SETTINGS.redis_url,
            redis_username=SETTINGS.redis_username,
            redis_password=SETTINGS.redis_password,
            redis_token_prefix="admin"
        )
    else:
        return AccessTokenStoreManager(
            store_type=SETTINGS.session_token_store_type,
            file_name=SETTINGS.user_api_tokens_file_name,
            redis_url=SETTINGS.redis_url,
            redis_username=SETTINGS.redis_username,
            redis_password=SETTINGS.redis_password,
            redis_token_prefix="user"
        )