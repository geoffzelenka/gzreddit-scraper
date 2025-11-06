#!/usr/bin/env python3

import re
import sys

from . import reddit
from . import stonkset

from collections import defaultdict
from datetime import datetime
from pprint import pprint


class WSBDailyWatcher:
    """Do some stats on the Daily Threads at WSB"""

    def __init__(self):
        self._ticker_pattern = re.compile(r'\b\$?[A-Za-z]{1,5}\b')
        self._stonks = stonkset.StonkSet()
        self._reddit = reddit.Reddit()

        self._stats = {
            "user_post_count": defaultdict(int),
            "ticker_count": defaultdict(int),
            "comments_processed": 0,
            }

    def clean_text(self, text):
        text = re.sub(r'http\S+', '', text)  # remove links
        text = re.sub(r'[^A-Za-z0-9$ .,!?\'"\-]+', ' ', text)
        return text.strip()

    def process_comment(self, comment):
        self._stats["comments_processed"] += 1
        if comment.author is not None:
            self._stats["user_post_count"][comment.author.name] += 1

        comment_text = self.clean_text(comment.body)
        tickers = self._ticker_pattern.findall(comment_text)
        tickers = [ t.upper().strip("$") for t in tickers if self._stonks.contains(t.strip("$")) ]
        for t in tickers:
            self._stats["ticker_count"][t] += 1

    def get_daily_thread_stats(self, thread_name):
        stickies = self._reddit.get_stickied_posts("wallstreetbets", thread_name)
        print(stickies)

        for sticky in stickies:
            print(f"Getting stats on {sticky.title}")
            sticky.comments.replace_more(limit=0) # this flattens the comment tree
            for comment in sticky.comments.list():
                self.process_comment(comment)
        return self._stats      


def main():

    now = datetime.now()
    if now.weekday() > 4: # make sure its not the weekend
        print("Its the weekend, no stonks")
        sys.exit(0)

    if 9 <= now.hour < 16: #Market hours(ish) 930am-4pm, check the daily thread
        thread_name = "Daily Discussion"
    else: # after hours
        thread_name = "Your Moves"


    wsb = WSBDailyWatcher()
    stats = wsb.get_daily_thread_stats(thread_name)

    print(f"Processed {stats["comments_processed"]} comments")
   
    print(f"Comments from {len(stats["user_post_count"])} redditors") 
    pprint(sorted(stats["user_post_count"].items(), key=lambda item: item[1], reverse=True))

    print(f"Comments mentioned {len(stats["ticker_count"])} different tickers")
    pprint(sorted(stats["ticker_count"].items(), key=lambda item: item[1], reverse=True))


if __name__ == "__main__":
    main()
