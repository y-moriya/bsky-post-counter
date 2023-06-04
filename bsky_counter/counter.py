from datetime import date
from logging import Logger

import atprototools
import requests

from bsky_counter import PostSummary
from bsky_counter.logger import BskyCounterLogger


class BskyCounter:

    def __init__(self, logger: Logger = None, debug=False):
        self._logger = logger if logger else BskyCounterLogger(debug).get_logger()

    def run(self, handle, password, target_date: date = None):
        session = atprototools.Session(handle, password)
        data = PostSummary(target_date=target_date) if target_date else PostSummary()

        cursor = None
        while True:
            response = self._fetch_posts(session, cursor)
            if response.status_code != 200:
                self._logger.warning(f"Something went wrong!\n{response.status_code}: {response.text}")
                break
            result = response.json()
            # cursor = result.get("cursor")
            for feed in result.get("feed"):
                post = feed.get("post")
                if not post:
                    continue
                data.total += 1
                if post.get("author", {}).get("did") != session.DID:
                    data.repost += 1
                    continue
                record = post.get("record", {})
                if record.get("reply"):
                    data.reply += 1
                if record.get("embed", {}).get("$type") == "app.bsky.embed.record":
                    data.quote += 1
            self._logger.debug(data)
            if not cursor:
                break

    @classmethod
    def _fetch_posts(cls, session, cursor):
        headers = {"Authorization": "Bearer " + session.ATP_AUTH_TOKEN}
        return requests.get(
            f"{session.ATP_HOST}/xrpc/app.bsky.feed.getAuthorFeed",
            headers=headers,
            params={"actor": session.DID,
                    "limit": 100,
                    "cursor": cursor}
        )
