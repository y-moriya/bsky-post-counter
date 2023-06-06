import json
from logging import Logger

import requests

from bsky_counter.data import PostSummary
from bsky_counter.logger import BskyCounterLogger


class Pixela:
    RETRY_COUNT = 5

    def __init__(self, logger: Logger = None):
        self._logger = logger if logger else BskyCounterLogger().get_logger()

    def post_to_pixela(self, user_name: str, token: str, graph_id: str, post_summary: PostSummary):
        if not (user_name and token and graph_id):
            return None
        endpoint = f"https://pixe.la/v1/users/{user_name}/graphs/{graph_id}"
        target_date = post_summary.target_date.strftime("%Y%m%d")
        payload = json.dumps({
            "date": target_date,
            "quantity": str(post_summary.total),
            "optionalData": json.dumps({
                "total": post_summary.total,
                "reply": post_summary.reply,
                "repost": post_summary.repost,
                "quote": post_summary.quote,
            }),
        })
        headers = {"X-USER-TOKEN": token}
        self._logger.debug(payload)

        self._post(endpoint, payload, headers)
        return endpoint

    def _post(self, endpoint, payload, headers, retry_count=0):
        if retry_count >= self.RETRY_COUNT:
            return False
        try:
            res = requests.post(endpoint, data=payload, headers=headers)
            self._logger.debug(f"{res.status_code}: {res.text}")
            if res.status_code == 503 and res.json().get("isRejected"):
                return self._post(endpoint, payload, headers, retry_count + 1)
            return res.status_code == 200
        except Exception as e:
            self._logger.exception(e)
            return False
