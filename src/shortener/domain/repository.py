from typing import Protocol

from shortener.domain.models import Link


class LinkRepository(Protocol):
    async def add(self, link: Link) -> None: ...

    async def get(self, code: str) -> Link | None: ...

    async def register_visit(self, code: str) -> Link | None: ...
