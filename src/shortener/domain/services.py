import secrets
import string
from datetime import UTC, datetime

from shortener.domain.errors import (
    CodeGenerationFailedError,
    DuplicatedCodeError,
    LinkNotFoundError,
)
from shortener.domain.models import Link
from shortener.domain.repository import LinkRepository

CODE_ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 7
MAX_CODE_ATTEMPTS = 5


class ShortenerService:
    def __init__(self, repository: LinkRepository) -> None:
        self._repository = repository

    async def shorten(self, target_url: str) -> Link:
        for _ in range(MAX_CODE_ATTEMPTS):
            link = Link(
                code=self._generate_code(),
                target_url=target_url,
                created_at=datetime.now(UTC),
            )
            try:
                await self._repository.add(link)
            except DuplicatedCodeError:
                continue
            return link
        raise CodeGenerationFailedError

    async def resolve(self, code: str) -> Link:
        link = await self._repository.register_visit(code)
        if link is None:
            raise LinkNotFoundError(code)
        return link

    async def stats(self, code: str) -> Link:
        link = await self._repository.get(code)
        if link is None:
            raise LinkNotFoundError(code)
        return link

    @staticmethod
    def _generate_code() -> str:
        return "".join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))
