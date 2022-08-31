from fastapi import Depends

from core.helper_classes.sqlAlchemyDBManager import SQLAlchemyDBManager
from api_dependencies.helper_classes.dependencies import Dependencies
from api_dependencies.helper_classes.cookie_extractor_for_oauth2_password import CookieExtractorWithOpenApiSecuritySchemeForOAuth2PasswordBearer
from api_dependencies.helper_classes.admin_cookie_extractor_for_oauth2_password import AdminCookieExtractorWithOpenApiSecuritySchemeForOAuth2PasswordBearer
from api_dependencies.validated_access_token import get_validated_access_token_as_fastapi_dependency
# from api_dependencies.validated_admin_access_token import get_validated_admin_access_token_as_fastapi_dependency
from api_dependencies.current_user import get_current_user_as_fastapi_dependency
from api_dependencies.current_admin_user import get_current_admin_user_as_fastapi_dependency
from data.access_tokens_store.access_token_store_manager import AccessTokenStoreManager

def get_api_routes_dependencies(
    app_db_manager: SQLAlchemyDBManager,
    access_token_store_manager: AccessTokenStoreManager
):
    db_session_as_dependency=Depends(app_db_manager.db_session)
    token_extractor = CookieExtractorWithOpenApiSecuritySchemeForOAuth2PasswordBearer(tokenUrl="api/login")
    token_extractor_as_dependency=Depends(token_extractor)
    access_token_store_as_dependency=Depends(access_token_store_manager.get_store)
    validated_access_token_as_dependency=get_validated_access_token_as_fastapi_dependency(token_extractor_as_dependency, access_token_store_as_dependency)
    current_user_as_dependency=get_current_user_as_fastapi_dependency(validated_access_token_as_dependency, db_session_as_dependency)
    route_dependencies = Dependencies(
        db_session_as_dependency=db_session_as_dependency,
        access_token_store_as_dependency=access_token_store_as_dependency,
        validated_access_token_as_dependency=validated_access_token_as_dependency,
        current_user_as_dependency=current_user_as_dependency
    )
    return route_dependencies

def get_admin_routes_dependencies(
    app_db_manager: SQLAlchemyDBManager,
    admin_access_token_store_manager: AccessTokenStoreManager
):
    db_session_as_dependency=Depends(app_db_manager.db_session)
    token_extractor = AdminCookieExtractorWithOpenApiSecuritySchemeForOAuth2PasswordBearer(tokenUrl="api/admin/login")
    token_extractor_as_dependency=Depends(token_extractor)
    access_token_store_as_dependency=Depends(admin_access_token_store_manager.get_store)
    validated_access_token_as_dependency=get_validated_access_token_as_fastapi_dependency(token_extractor_as_dependency, access_token_store_as_dependency)
    current_user_as_dependency=get_current_admin_user_as_fastapi_dependency(validated_access_token_as_dependency, db_session_as_dependency)
    route_dependencies = Dependencies(
        db_session_as_dependency=db_session_as_dependency,
        access_token_store_as_dependency=access_token_store_as_dependency,
        validated_access_token_as_dependency=validated_access_token_as_dependency,
        current_user_as_dependency=current_user_as_dependency
    )
    return route_dependencies
