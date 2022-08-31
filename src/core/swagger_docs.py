from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

from admin.api.routes import add_all_admin_resources_routes
from api.non_admin_routes import add_non_admin_routes
from api_dependencies.helper_classes.dependencies import Dependencies

def create_swagger_docs_for_regular_endpoints(
    app: FastAPI,
    regular_api_routes_dependencies: Dependencies,
    samesite: str,
    secure_cookies: bool,
):
    @app.get("/openapi.json")
    async def get_open_api_endpoint():
        _router = APIRouter(prefix="/api")
        add_non_admin_routes(_router, regular_api_routes_dependencies, samesite, secure_cookies)
        return JSONResponse(get_openapi(title="FastAPI", version=1, routes=_router.routes))
    @app.get("/docs")
    async def get_documentation():
        return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


def create_swagger_docs_for_admin_endpoints(
    app: FastAPI,
    admin_api_routes_dependencies: Dependencies,
    secure_cookies: bool,
):
    @app.get("/admin-openapi.json")
    async def get_open_api_endpoint():
        _router = APIRouter(prefix="/api")
        add_all_admin_resources_routes(_router, admin_api_routes_dependencies, secure_cookies)
        return JSONResponse(get_openapi(title="FastAPI", version=1, routes=_router.routes))
    @app.get("/admin-docs")
    async def get_documentation():
        return get_swagger_ui_html(openapi_url="/admin-openapi.json", title="docs")
