from fastapi import FastAPI

from helpers_classes.spa_static_files import SPAStaticFiles


def mount_app(app: FastAPI):
    app.mount(
        "/admin",
        SPAStaticFiles(directory="admin_app/vue_admin_html", html=True),
        name="admin_app",
    )
