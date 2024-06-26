from fastapi import Depends
from sqlalchemy.orm import Session

from data.database.models.admin_user import AdminUser as AdminUserModel
from stores.sql_db_store import crud_base
from utils.security.access_token_utils import parse_access_token


def get_current_admin_user_as_fastapi_dependency(
    get_validated_token_as_fastapi_dependency: str,
    get_db_session_as_fastapi_dependency: Session,
):
    def current_admin_user(
        access_token: str = get_validated_token_as_fastapi_dependency,
        sql_db_session: Session = get_db_session_as_fastapi_dependency,
    ):
        admin_user_id = parse_access_token(access_token, "user_id")
        return crud_base.get_resource_item(
            sql_db_session, AdminUserModel, admin_user_id
        )

    return Depends(current_admin_user)
