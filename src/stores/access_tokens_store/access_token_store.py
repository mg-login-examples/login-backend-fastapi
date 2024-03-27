from abc import ABC, abstractmethod
import logging

from utils.security.access_token_utils import check_access_token_in_valid_format, check_access_token_is_expired

logger = logging.getLogger(__name__)


class AccessTokenStore(ABC):

    @abstractmethod
    async def add_access_token(self, user_id: int, access_token: str):
        return

    @abstractmethod
    async def remove_access_token(self, user_id: int, access_token: str):
        return

    @abstractmethod
    async def check_if_access_token_is_valid(self, access_token: str):
        is_token_valid = False
        if check_access_token_in_valid_format(access_token):
            if not check_access_token_is_expired(access_token):
                is_token_valid = True
        return is_token_valid
