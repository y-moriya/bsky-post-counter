from datetime import date, datetime
from logging import Logger
from typing import Optional
from zoneinfo import ZoneInfo

import atprototools
import requests

from bsky_counter.data import PostSummary
from bsky_counter.logger import BskyCounterLogger


class BskyCounter:
    INDEXED_AT_FMT = "%Y-%m-%dT%H:%M:%S.%f%z"

    def __init__(self, handle, password, timezone: ZoneInfo, logger: Logger = None):
        self._logger = logger if logger else BskyCounterLogger().get_logger()
        self._timezone = timezone
        self._session = atprototools.Session(handle, password)

    def run(self, target_date: date):
        data = PostSummary(target_date=target_date)

        cursor = None
        while True:
            response = self._fetch_posts(cursor)
            if response.status_code != 200:
                self._logger.warning(f"Something went wrong!\n{response.status_code}: {response.text}")
                break
            result = response.json()
            cursor = result.get("cursor")
            fetch_next, data = self._aggregate_posts(data, self._session.DID, result.get("feed"))
            if not (cursor and fetch_next):
                break
        self._logger.debug(data)
        return data

    def _fetch_posts(self, cursor):
        headers = {"Authorization": "Bearer " + self._session.ATP_AUTH_TOKEN}
        return requests.get(
            f"{self._session.ATP_HOST}/xrpc/app.bsky.feed.getAuthorFeed",
            headers=headers,
            params={"actor": self._session.DID,
                    "limit": 100,
                    "cursor": cursor}
        )

    def _aggregate_posts(self, summary: PostSummary, author_did: str, feeds: list) -> (bool, PostSummary):
        if not feeds:
            return False, summary
        for feed in feeds:
            post = feed.get("post")
            if not post:
                continue
            post_date = self._date_from_str(post.get("indexedAt"))
            if not post_date or post_date > summary.target_date:
                # parse error or future date
                continue
            if post_date < summary.target_date:
                # past date
                return False, summary
            summary.total += 1
            if post.get("author", {}).get("did") != author_did:
                summary.repost += 1
                continue
            record = post.get("record", {})
            if record.get("reply"):
                summary.reply += 1
            if record.get("embed", {}).get("$type") == "app.bsky.embed.record":
                summary.quote += 1
        return True, summary

    def _date_from_str(self, indexed_at: str) -> Optional[date]:
        try:
            return datetime.strptime(indexed_at, self.INDEXED_AT_FMT).astimezone(self._timezone).date()
        except:
            return None

    def post_result(self, result: PostSummary, pixela_endpoint: str):
        content = f"{result.target_date:%Y-%m-%d}\n" + \
                  f"total: {result.total}\n" + \
                  f"repost: {result.repost}\n" + \
                  f"reply: {result.reply}\n" + \
                  f"quote: {result.quote}\n\n" + \
                  pixela_endpoint
        self._logger.debug(content)
        self._session.postBloot(content)
