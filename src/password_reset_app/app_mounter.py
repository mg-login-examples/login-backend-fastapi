from fastapi import FastAPI
from helpers_classes.spa_static_files import SPAStaticFiles


def mount_app(app: FastAPI):
    app.mount(
        "/password-reset",
        SPAStaticFiles(
            directory="password_reset_app/vue_password_reset_html", html=True
        ),
        name="password_reset_app",
    )
