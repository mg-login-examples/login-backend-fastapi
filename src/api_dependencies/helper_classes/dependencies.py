from typing import Any

from sqlalchemy.orm import Session

from data.access_tokens_store.helper_classes.access_token_store import AccessTokenStore
from data.schemas.users.user import User

class Dependencies:
    def __init__(
        self,
        db_session_as_dependency: Session = None,
        access_token_store_as_dependency: AccessTokenStore = None,
        validated_access_token_as_dependency: str = None,
        current_user_as_dependency: User = None,
        restrict_endpoint_to_own_resources_param_item_id_as_dependency: Any = None,
        restrict_endpoint_to_own_resources_param_user_id_as_dependency: Any = None,
    ):
        self.db = db_session_as_dependency
        self.access_token_store = access_token_store_as_dependency
        self.validated_access_token = validated_access_token_as_dependency
        self.current_user = current_user_as_dependency
        self.restrict_endpoint_to_own_resources_param_item_id = restrict_endpoint_to_own_resources_param_item_id_as_dependency
        self.restrict_endpoint_to_own_resources_param_user_id = restrict_endpoint_to_own_resources_param_user_id_as_dependency
