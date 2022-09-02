from fastapi import Depends
from sqlalchemy.orm import Session

from utils.security.access_token_utils import parse_access_token
from data.database.models.admin_user import AdminUser as AdminUserModel

from crud_endpoints_generator import crud_base

def get_current_admin_user_as_fastapi_dependency(
    get_validated_token_as_fastapi_dependency: str,
    get_db_session_as_fastapi_dependency: Session
):
    def current_admin_user(
        access_token: str = get_validated_token_as_fastapi_dependency,
        db: Session = get_db_session_as_fastapi_dependency
    ):
        admin_user_id = parse_access_token(access_token, "user_id")
        return crud_base.get_resource_item(db, AdminUserModel, admin_user_id)

    return Depends(current_admin_user)
