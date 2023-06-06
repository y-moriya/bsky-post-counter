from dataclasses import dataclass, field
from datetime import date, timedelta, datetime
from zoneinfo import ZoneInfo


def _default_target_date():
    return date.today() - timedelta(days=1)


def last_date_with_tz(tz: ZoneInfo):
    return (datetime.now(tz) - timedelta(days=1)).date()


@dataclass
class PostSummary:
    target_date: date = field(default_factory=_default_target_date, repr=False)
    total: int = 0
    repost: int = 0
    reply: int = 0
    quote: int = 0
