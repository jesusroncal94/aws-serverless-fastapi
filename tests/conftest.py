from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from shortener.api.dependencies import get_service
from shortener.config import Settings
from shortener.domain.services import ShortenerService
from shortener.main import create_app
from tests.doubles import InMemoryLinkRepository


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    app = create_app(Settings(base_url="http://testserver"))
    repository = InMemoryLinkRepository()
    app.dependency_overrides[get_service] = lambda: ShortenerService(repository)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
