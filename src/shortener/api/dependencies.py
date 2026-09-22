from typing import Annotated

from fastapi import Depends, Request

from shortener.domain.services import ShortenerService
from shortener.infrastructure.dynamodb_link_repository import DynamoDbLinkRepository


def get_service(request: Request) -> ShortenerService:
    return ShortenerService(DynamoDbLinkRepository(request.app.state.table))


def get_base_url(request: Request) -> str:
    configured = request.app.state.settings.base_url
    return configured or str(request.base_url).rstrip("/")


ServiceDep = Annotated[ShortenerService, Depends(get_service)]
BaseUrlDep = Annotated[str, Depends(get_base_url)]
