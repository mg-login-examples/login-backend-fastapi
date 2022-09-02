from fastapi import Depends
from sqlalchemy.orm import Session

from utils.security.access_token_utils import parse_access_token
from data.database.models.user import User as UserModel
from crud_endpoints_generator import crud_base

def get_current_user_as_fastapi_dependency(
    get_validated_token_as_fastapi_dependency: str,
    get_db_session_as_fastapi_dependency: Session
):
    def current_user_as_fastapi(
        access_token: str = get_validated_token_as_fastapi_dependency,
        db: Session = get_db_session_as_fastapi_dependency
    ):
        user_id = parse_access_token(access_token, "user_id")
        return crud_base.get_resource_item(db, UserModel, user_id)

    return Depends(current_user_as_fastapi)
