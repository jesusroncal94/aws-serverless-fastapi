from dataclasses import replace

from shortener.domain.errors import DuplicatedCodeError
from shortener.domain.models import Link


class InMemoryLinkRepository:
    def __init__(self) -> None:
        self._links: dict[str, Link] = {}

    async def add(self, link: Link) -> None:
        if link.code in self._links:
            raise DuplicatedCodeError(link.code)
        self._links[link.code] = link

    async def get(self, code: str) -> Link | None:
        return self._links.get(code)

    async def register_visit(self, code: str) -> Link | None:
        link = self._links.get(code)
        if link is None:
            return None
        visited = replace(link, visits=link.visits + 1)
        self._links[code] = visited
        return visited
