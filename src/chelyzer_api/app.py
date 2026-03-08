from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chelyzer_api.routes import routers


def create_app() -> FastAPI:
    """Return a new app instance."""
    app = FastAPI()

    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    for route in routers:
        app.include_router(route)

    return app
