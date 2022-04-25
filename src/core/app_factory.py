import logging

from fastapi import FastAPI, Depends

from core.cors_settings import add_cors
from api.routes import add_routes
from admin.view.mount_admin_app import mount_admin_app
from core.helper_classes.sqlAlchemyDBManager import SQLAlchemyDBManager
from api_dependencies.helper_classes.dependencies import Dependencies
from api_dependencies.helper_classes.cookie_extractor_for_oauth2_password import CookieExtractorWithOpenApiSecuritySchemeForOAuth2PasswordBearer
from api_dependencies.validated_access_token import get_validated_access_token_as_fastapi_dependency
from api_dependencies.current_user import get_current_user_as_fastapi_dependency

logger = logging.getLogger(__name__)

def create_app(app_db_manager: SQLAlchemyDBManager, add_admin_app: bool = False) -> FastAPI:
    app = FastAPI()

    add_cors(app)

    db_session_as_dependency=Depends(app_db_manager.db_session)
    token_extractor = CookieExtractorWithOpenApiSecuritySchemeForOAuth2PasswordBearer(tokenUrl="api/login")
    token_extractor_as_fastapi_dependency=Depends(token_extractor)
    validated_access_token_as_dependency=get_validated_access_token_as_fastapi_dependency(token_extractor_as_fastapi_dependency)
    current_user_as_dependency=get_current_user_as_fastapi_dependency(validated_access_token_as_dependency, db_session_as_dependency)
    route_dependencies = Dependencies(
        db_session_as_dependency=db_session_as_dependency,
        validated_access_token_as_dependency=validated_access_token_as_dependency,
        current_user_as_dependency=current_user_as_dependency
    )
    add_routes(app, app_db_manager.db_session, route_dependencies, add_admin_app)

    if add_admin_app:
        mount_admin_app(app)

    return app
