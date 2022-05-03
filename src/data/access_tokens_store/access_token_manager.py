import logging

from utils.security.access_token_utils import parse_access_token, check_access_token_is_expired
from data.access_tokens_store.access_token_file_store import AccessTokenFileStore

logger = logging.getLogger(__name__)


class AccessTokenManager:

    def __init__(self, store_type = "in_memory_db", in_memory_db_configs=None, file_name: str=None):
        self.story_type = store_type
        if store_type == "file":
            self.file_store = AccessTokenFileStore(file_name)
        else:
            self.in_memory_db_configs = in_memory_db_configs
            # in_memory_db_utils.init_store(self.in_memory_db_configs.url)

    def add_access_token(self, user_id: int, access_token: str):
        logger.info("***********")
        logger.info(access_token)
        self.file_store.add_access_token_if_not_found(user_id, access_token)

    def remove_access_token(self, user_id: int, access_token: str):
        self.file_store.remove_access_token(user_id, access_token)

    def check_if_access_token_is_valid(self, access_token: str):
        # TODO Sanitize access_token
        # TODO Check token format is correct
        token_user_id = parse_access_token(access_token, "user_id")
        is_token_valid = False
        if not check_access_token_is_expired(access_token):
            if self.file_store.check_access_token_exists(token_user_id, access_token):
                is_token_valid = True
        return is_token_valid
