from datetime import datetime

from pydantic import BaseModel, HttpUrl

from shortener.domain.models import Link


class ShortenRequest(BaseModel):
    target_url: HttpUrl


class LinkResponse(BaseModel):
    code: str
    short_url: str
    target_url: str
    created_at: datetime
    visits: int

    @classmethod
    def from_domain(cls, link: Link, base_url: str) -> "LinkResponse":
        return cls(
            code=link.code,
            short_url=f"{base_url.rstrip('/')}/{link.code}",
            target_url=link.target_url,
            created_at=link.created_at,
            visits=link.visits,
        )
