from fastapi import FastAPI
from starlette.staticfiles import StaticFiles, Scope, Response


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: Scope) -> Response:
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response('.', scope)
        return response

def mount_admin_app(app: FastAPI):
    app.mount("/admin", SPAStaticFiles(directory="admin_app/vue_admin_html", html=True), name="admin_app")
