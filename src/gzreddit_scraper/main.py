#!/usr/bin/env python3

import re

from . import reddit
from . import stonkset

from collections import defaultdict
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

    def get_daily_thread_stats(self):
        stickies = self._reddit.get_stickied_posts("wallstreetbets","Your Moves")
        print(stickies)

        for sticky in stickies:
            print(f"Getting stats on {sticky.title}")
            sticky.comments.replace_more(limit=0) # this flattens the comment tree
            for comment in sticky.comments.list():
                self.process_comment(comment)
                  
            print(f"Processed {self._stats["comments_processed"]} comments")
        
        print(f"Comments from {len(self._stats["user_post_count"])} redditors") 
        pprint(sorted(self._stats["user_post_count"].items(), key=lambda item: item[1], reverse=True))

        print(f"Comments mentioned {len(self._stats["ticker_count"])} different tickers")
        pprint(sorted(self._stats["ticker_count"].items(), key=lambda item: item[1], reverse=True))




if __name__ == "__main__":
    wsb = WSBDailyWatcher()
    wsb.get_daily_thread_stats()
    
