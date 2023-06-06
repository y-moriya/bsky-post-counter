import argparse
import os
import zoneinfo
from datetime import datetime, timedelta

from bsky_counter.counter import BskyCounter
from bsky_counter.logger import BskyCounterLogger
from bsky_counter.pixela import Pixela


def parse_args():
    parser = argparse.ArgumentParser(description="""Count Bsky Post\n
    set environment variables:\n
      `BSKY_PASSWORD`for bluesky password\n
      `PIXELA_API_TOKEN` for post to pixela
    """)
    parser.add_argument("-u", "--handle", required=True, help="handle or mail address or did to login to bsky")
    parser.add_argument("-t", "--timezone", default="utc", help="set your timezone")
    parser.add_argument("-d", "--date", help="set target date(YYYY-MM-DD)")
    parser.add_argument("--post-summary", help="post the result to bluesky if this flag is set", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-vv", "--debug", action="store_true")
    parser.add_argument("-p", "--pixela-user", help="set pixela username")
    parser.add_argument("-g", "--pixela-graph-id", help="set pixela graph id")

    setting = parser.parse_args()
    setting.tz = zoneinfo.ZoneInfo(setting.timezone)
    if setting.date:
        setting.target_date = datetime.strptime(setting.date, "%Y-%m-%d").date()
    else:
        setting.target_date = (datetime.now(setting.tz) - timedelta(days=1)).date()
    setting.password = os.getenv("BSKY_PASSWORD")
    setting.pixela_token = os.getenv("PIXELA_API_TOKEN")
    return setting


def run():
    setting = parse_args()
    bsky_logger = BskyCounterLogger(info=setting.verbose, debug=setting.debug).get_logger()
    c = BskyCounter(setting.handle, setting.password, setting.tz, logger=bsky_logger)
    result = c.run(setting.target_date)

    endpoint = ""
    if setting.pixela_user and setting.pixela_graph_id and setting.pixela_token:
        p = Pixela(logger=bsky_logger)
        endpoint = p.post_to_pixela(setting.pixela_user,
                                    setting.pixela_token,
                                    setting.pixela_graph_id,
                                    result)

    if setting.post_summary:
        c.post_result(result, endpoint)
