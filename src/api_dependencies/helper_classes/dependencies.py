from sqlalchemy.orm import Session
from data.schemas.users.user import User

class Dependencies:
    def __init__(
        self,
        db_session_as_dependency: Session = None,
        validated_access_token_as_dependency: str = None,
        current_user_as_dependency: User = None
    ):
        self.db = db_session_as_dependency
        self.validated_access_token = validated_access_token_as_dependency
        self.current_user = current_user_as_dependency
