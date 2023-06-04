from dataclasses import dataclass, field, asdict
from datetime import date, timedelta


def _default_target_date():
    return date.today() - timedelta(days=1)


@dataclass
class PostSummary:
    target_date: date = field(default_factory=_default_target_date, repr=False)
    total: int = 0
    repost: int = 0
    reply: int = 0
    quote: int = 0
