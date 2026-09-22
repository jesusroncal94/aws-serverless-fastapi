from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Link:
    code: str
    target_url: str
    created_at: datetime
    visits: int = 0
