from fastapi import Depends

from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from stores.redis_store.aioredis_cache_manager import AioRedisCacheManager
from stores.nosql_db_store.pymongo_manager import get_db as get_nosql_db
from api_dependencies.common_route_dependencies import CommonRouteDependencies
from api_dependencies.dependencies.nosql_db import get_nosql_db_as_fastapi_dependency
from api_dependencies.dependencies.helper_classes.user_access_token_extractor import UserAccessTokenExtractor
from api_dependencies.dependencies.helper_classes.admin_access_token_extractor import AdminAccessTokenExtractor
from api_dependencies.dependencies.validated_access_token import get_validated_access_token_as_fastapi_dependency
from api_dependencies.dependencies.current_user import get_current_user_as_fastapi_dependency
from api_dependencies.dependencies.current_admin_user import get_current_admin_user_as_fastapi_dependency
from api_dependencies.dependencies.restrict_endpoint_to_own_resources_param_item_id_dependency import get_restrict_endpoint_to_own_resources_param_item_id_as_fastapi_dependency
from api_dependencies.dependencies.restrict_endpoint_to_own_resources_param_user_id_dependency import get_restrict_endpoint_to_own_resources_param_user_id_as_fastapi_dependency
from api_dependencies.dependencies.access_token_store import get_access_token_store_as_fastapi_dependency
from core.helper_classes.settings import Settings

def get_user_routes_dependencies(
    app_db_manager: SQLAlchemyDBManager,
    app_cache_manager: AioRedisCacheManager,
    settings: Settings,
):
    db_session_as_dependency=Depends(app_db_manager.db_session)
    cache_session_as_dependency=Depends(app_cache_manager.redis_session)
    nosql_database_as_dependency=get_nosql_db_as_fastapi_dependency(
        settings.mongo_host,
        settings.mongo_port,
        settings.mongo_username,
        settings.mongo_password,
        settings.mongo_database,
    )
    token_extractor = UserAccessTokenExtractor(tokenUrl="api/login")
    token_extractor_as_dependency=Depends(token_extractor)
    access_token_store_as_dependency=get_access_token_store_as_fastapi_dependency(
        store_type=settings.access_tokens_store_type,
        redis_session_as_fastapi_dependency=cache_session_as_dependency,
        redis_token_prefix="user",
        file_name="user_access_tokens.txt",
    )
    validated_access_token_as_dependency=get_validated_access_token_as_fastapi_dependency(token_extractor_as_dependency, access_token_store_as_dependency)
    current_user_as_dependency=get_current_user_as_fastapi_dependency(validated_access_token_as_dependency, db_session_as_dependency)
    restrict_endpoint_to_own_resources_param_item_id_as_dependency = get_restrict_endpoint_to_own_resources_param_item_id_as_fastapi_dependency(current_user_as_dependency)
    restrict_endpoint_to_own_resources_param_user_id_as_dependency = get_restrict_endpoint_to_own_resources_param_user_id_as_fastapi_dependency(current_user_as_dependency)
    route_dependencies = CommonRouteDependencies(
        db_session_as_dependency=db_session_as_dependency,
        cache_session_as_dependency=cache_session_as_dependency,
        nosql_database_as_dependency=nosql_database_as_dependency,
        access_token_store_as_dependency=access_token_store_as_dependency,
        validated_access_token_as_dependency=validated_access_token_as_dependency,
        current_user_as_dependency=current_user_as_dependency,
        restrict_endpoint_to_own_resources_param_item_id_as_dependency=restrict_endpoint_to_own_resources_param_item_id_as_dependency,
        restrict_endpoint_to_own_resources_param_user_id_as_dependency=restrict_endpoint_to_own_resources_param_user_id_as_dependency,
    )
    return route_dependencies

def get_admin_routes_dependencies(
    app_db_manager: SQLAlchemyDBManager,
    app_cache_manager: AioRedisCacheManager,
    settings: Settings,
):
    db_session_as_dependency=Depends(app_db_manager.db_session)
    cache_session_as_dependency=Depends(app_cache_manager.redis_session)
    token_extractor = AdminAccessTokenExtractor(tokenUrl="api/admin/login")
    token_extractor_as_dependency=Depends(token_extractor)
    access_token_store_as_dependency=get_access_token_store_as_fastapi_dependency(
        store_type=settings.access_tokens_store_type,
        redis_session_as_fastapi_dependency=cache_session_as_dependency,
        redis_token_prefix="admin",
        file_name="admin_access_tokens.txt",
    )
    validated_access_token_as_dependency=get_validated_access_token_as_fastapi_dependency(token_extractor_as_dependency, access_token_store_as_dependency)
    current_user_as_dependency=get_current_admin_user_as_fastapi_dependency(validated_access_token_as_dependency, db_session_as_dependency)
    route_dependencies = CommonRouteDependencies(
        db_session_as_dependency=db_session_as_dependency,
        cache_session_as_dependency=cache_session_as_dependency,
        access_token_store_as_dependency=access_token_store_as_dependency,
        validated_access_token_as_dependency=validated_access_token_as_dependency,
        current_user_as_dependency=current_user_as_dependency
    )
    return route_dependencies
