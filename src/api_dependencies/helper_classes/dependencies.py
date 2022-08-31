from sqlalchemy.orm import Session

from data.access_tokens_store.helper_classes.access_token_store import AccessTokenStore
from data.schemas.users.user import User

class Dependencies:
    def __init__(
        self,
        db_session_as_dependency: Session = None,
        access_token_store_as_dependency: AccessTokenStore = None,
        validated_access_token_as_dependency: str = None,
        current_user_as_dependency: User = None
    ):
        self.db = db_session_as_dependency
        self.access_token_store = access_token_store_as_dependency
        self.validated_access_token = validated_access_token_as_dependency
        self.current_user = current_user_as_dependency
