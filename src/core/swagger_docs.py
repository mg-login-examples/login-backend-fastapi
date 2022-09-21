from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

from rest_endpoints.admin import routes as admin_routes
from rest_endpoints.user import routes as user_routes
from api_dependencies.common_route_dependencies import CommonRouteDependencies

def create_swagger_docs_for_user_endpoints(
    app: FastAPI,
    regular_api_routes_dependencies: CommonRouteDependencies,
    samesite: str,
    secure_cookies: bool,
):
    @app.get("/openapi.json")
    async def get_open_api_endpoint():
        base_router = APIRouter(prefix="/api")
        user_router = user_routes.get_router(regular_api_routes_dependencies, samesite, secure_cookies)
        base_router.include_router(user_router)
        return JSONResponse(get_openapi(title="FastAPI", version=1, routes=base_router.routes))
    @app.get("/docs")
    async def get_documentation():
        return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


def create_swagger_docs_for_admin_endpoints(
    app: FastAPI,
    admin_api_routes_dependencies: CommonRouteDependencies,
    secure_cookies: bool,
):
    @app.get("/admin-openapi.json")
    async def get_open_api_endpoint():
        base_router = APIRouter(prefix="/api")
        admin_router =  admin_routes.get_router(admin_api_routes_dependencies, secure_cookies)
        base_router.include_router(admin_router)
        return JSONResponse(get_openapi(title="FastAPI", version=1, routes=base_router.routes))
    @app.get("/admin-docs")
    async def get_documentation():
        return get_swagger_ui_html(openapi_url="/admin-openapi.json", title="docs")
