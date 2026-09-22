import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import aioboto3
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from shortener.api.routes import health_router, links_router, redirect_router
from shortener.config import Settings, get_settings
from shortener.domain.errors import LinkNotFoundError


async def handle_link_not_found(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    logging.basicConfig(level=settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        session = aioboto3.Session()
        async with session.resource(
            "dynamodb",
            region_name=settings.aws_region,
            endpoint_url=settings.dynamodb_endpoint_url,
        ) as dynamodb:
            app.state.table = await dynamodb.Table(settings.table_name)
            yield

    app = FastAPI(title="URL Shortener", version="1.0.0", lifespan=lifespan)
    app.state.settings = settings
    app.add_exception_handler(LinkNotFoundError, handle_link_not_found)
    app.include_router(health_router)
    app.include_router(links_router)
    app.include_router(redirect_router)
    return app


app = create_app()
