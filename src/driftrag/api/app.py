"""FastAPI application factory."""

from fastapi import FastAPI
from pydantic import BaseModel

from driftrag import __version__
from driftrag.config import get_settings


class HealthResponse(BaseModel):
    status: str
    version: str
    env: str


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Drift-Aware RAG", version=__version__)

    @app.get("/health", response_model=HealthResponse, tags=["ops"])
    def health() -> HealthResponse:
        return HealthResponse(status="ok", version=__version__, env=settings.env)

    return app


app = create_app()
