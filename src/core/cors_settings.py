from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

development_origins = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8019",
    "http://localhost:5173",
    "http://localhost:4173",
    "http://frontend.login.com:8029",
    "http://frontend.login.com:8030",
    "http://frontend.full_app_proxy.com",
]

cloud_development_origins = [
    "http://frontend.login-example.duckdns.org",
    "https://frontend.login-example.duckdns.org",
]

production_origins: list[str] = []


def add_cors(app: FastAPI, cors_origins_set: str):
    origins = []
    if cors_origins_set == "Development":
        origins = development_origins
    elif cors_origins_set == "Cloud-Development":
        origins = cloud_development_origins
    elif cors_origins_set == "Production":
        origins = production_origins

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
