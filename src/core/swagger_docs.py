from fastapi import APIRouter, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from api_dependencies.admin_route_dependencies import AdminRouteDependencies
from api_dependencies.user_route_dependencies import UserRouteDependencies
from rest_endpoints.admin import routes as admin_routes
from rest_endpoints.user import routes as user_routes


def create_swagger_docs_for_user_endpoints(
    app: FastAPI,
    user_route_dependencies: UserRouteDependencies,
    auth_cookie_type: str,
):
    @app.get("/openapi.json")
    async def get_open_api_endpoint():
        base_router = APIRouter(prefix="/api")
        user_router = user_routes.get_router(user_route_dependencies, auth_cookie_type)
        base_router.include_router(user_router)
        return JSONResponse(
            get_openapi(title="User API", version="1", routes=base_router.routes)
        )

    @app.get("/docs")
    @app.get("/docs/")
    async def get_documentation():
        return get_swagger_ui_html(openapi_url="/openapi.json", title="user-docs")


def create_swagger_docs_for_admin_endpoints(
    app: FastAPI,
    admin_routes_dependencies: AdminRouteDependencies,
    auth_cookie_type: str,
):
    @app.get("/admin-openapi.json")
    async def get_open_api_endpoint():
        base_router = APIRouter(prefix="/api")
        admin_router = admin_routes.get_router(
            admin_routes_dependencies, auth_cookie_type
        )
        base_router.include_router(admin_router)
        return JSONResponse(
            get_openapi(title="Admin API", version="1", routes=base_router.routes)
        )

    @app.get("/admin-docs")
    @app.get("/admin-docs/")
    async def get_documentation():
        return get_swagger_ui_html(
            openapi_url="/admin-openapi.json", title="admin-docs"
        )
