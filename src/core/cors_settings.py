from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

development_origins = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8019",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://127.0.0.1:8019",
    "https://login-frontend.localhost",
]

cloud_development_origins = [
    "http://login-frontend.duckdns.org",
    "https://login-frontend.duckdns.org",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8019",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://127.0.0.1:8019",
    "https://login-frontend.localhost",
]

production_origins = []

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
        allow_methods=['*'],
        allow_headers=['*'],
    )
